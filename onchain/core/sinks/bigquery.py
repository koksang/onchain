"""BigQuery Sink"""

import json
from typing import Iterable, Union, Iterator, Generator
from google.protobuf import descriptor_pb2
from google.cloud.bigquery_storage import (
    BigQueryWriteClient,
    AppendRowsRequest,
    WriteStream,
    ProtoRows,
    ProtoSchema,
    types,
)
from onchain.core.sinks.base import BaseSink
from onchain.core.mappers.proto import ProtoMapper
from onchain.core.logger import log

PROTO_DESCRIPTOR = descriptor_pb2.DescriptorProto()


class BigQuerySink(BaseSink):
    def __init__(self, config: dict, mapper: ProtoMapper) -> None:
        """Init

        Args:
            config (dict): BigQuery sink config
        """
        self.config = config
        self.mapper = mapper
        self.client, self.mapper = None, None
        log.info(f"Initiated {self._name} with config: {self.config}")

    def connect(self, reconnect: bool = False) -> None:
        """Establish client connection

        Args:
            reconnect (bool, optional): To reconnect the client?. Defaults to False.
        """
        if not (self.client and reconnect) or reconnect:
            self.client = BigQueryWriteClient()
            log.info("Connected to BigQuery client")

    def create_stream(self) -> WriteStream:
        """Create write stream

        Returns:
            WriteStream: Write stream object
        """
        client_config = self.config.get("client")
        project, dataset, table = (
            client_config["project"],
            client_config["datasedt"],
            client_config["table"],
        )
        parent = self.client.table_path(project, dataset, table)
        stream: WriteStream = self.client.create_write_stream(
            parent=parent, write_stream=WriteStream(type_=WriteStream.Type.COMMITTED)
        )
        log.info(
            f"Initiated write_stream: {stream.name}, parent: {parent}, type: COMMITTED!"
        )
        return stream

    def _generate_requests(
        self,
        stream: WriteStream,
        proto_schema: ProtoSchema,
        items: Union[Iterable[str], list[str]],
        send_limit: int,
    ) -> Generator[Iterator[AppendRowsRequest], None, None]:
        """Generate requests

        Args:
            stream (WriteStream): BigQuery write stream
            proto_schema (ProtoSchema): Protobuf model schema
            items (Union[Iterable[str], list[str]]): Messages to write
            send_limit (int): Chunking limit

        Yields:
            Generator[Iterator[AppendRowsRequest], None, None]: _description_
        """
        send_count = 0
        messages = types.ProtoRows()
        for item in items:
            item = json.loads(item) if isinstance(item, str) else item
            messages.serialized_rows.append(
                self.mapper.json_to_proto(item).SerializeToString()
            )
            send_count += 1
            if send_count % send_limit == 0:
                data = AppendRowsRequest.ProtoData(
                    writer_schema=proto_schema, rows=ProtoRows(serialized_rows=messages)
                )

                yield iter(
                    [AppendRowsRequest(write_stream=stream.name, proto_rows=data)]
                )

        data = AppendRowsRequest.ProtoData(
            writer_schema=proto_schema, rows=ProtoRows(serialized_rows=messages)
        )
        yield iter([AppendRowsRequest(write_stream=stream.name, proto_rows=data)])

    def write(
        self, items: Union[Iterable[str], list[str]], send_limit: int = 10
    ) -> None:
        """Write using producer

        Args:
            items (Union[Iterable[str], list[str]]): Messages to write
            send_limit (int): Chunking limit
        """
        if not self.client:
            self.connect()

        stream = self.create_stream()
        self.mapper.model.DESCRIPTOR.CopyToProto(PROTO_DESCRIPTOR)
        PROTO_SCHEMA = ProtoSchema(proto_descriptor=PROTO_DESCRIPTOR)

        request_generator = self._generate_requests(
            stream=stream, proto_schema=PROTO_SCHEMA, items=items, send_limit=send_limit
        )

        for resp in self.client.append_rows(requests=request_generator):
            log.debug(resp)
