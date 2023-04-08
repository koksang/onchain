"""BigQuery Sink"""

from typing import Iterable, Iterator, Generator
from google.protobuf import descriptor_pb2
from google.cloud.bigquery_storage import (
    BigQueryWriteClient,
    AppendRowsRequest,
    WriteStream,
    ProtoRows,
    ProtoSchema,
    types,
)
from google.protobuf.pyext.cpp_message import GeneratedProtocolMessageType
from onchain.core.base import BaseConnectionModule
from onchain.utils.helpers import decode_b64_json_string
from onchain.logger import log
from onchain.constants import GOOGLE_APPLICATION_CREDENTIALS_B64


class BigQuerySink(BaseConnectionModule):
    def __init__(
        self,
        client_config: dict,
        blockchain_name: str,
        blockchain_data: str,
        **kwargs,
    ) -> None:
        """Init

        Args:
            client_config (dict): BigQuery client configuration.
            blockchain_name (str): Blockchain name.
            blockchain_data (str): Blockchain data.
        """
        self._client_config = client_config
        super().__init__(blockchain_name, blockchain_data)

    def connect(self, reconnect: bool = False) -> None:
        """Establish client connection

        Args:
            reconnect (bool, optional): To reconnect the client?. Defaults to False.
        """
        # NOTE: Temporarily supporting GOOGLE_APPLICATION_CREDENTIALS or application default
        if not (self.client and reconnect) or reconnect:
            if GOOGLE_APPLICATION_CREDENTIALS_B64:
                credentials = decode_b64_json_string(GOOGLE_APPLICATION_CREDENTIALS_B64)
                self.client = BigQueryWriteClient(credentials=credentials)
            else:
                self.client = BigQueryWriteClient()
            log.info("Connected to BigQuery client")

    def create_stream(self) -> WriteStream:
        """Create write stream

        Returns:
            WriteStream: Write stream object
        """
        project, dataset, table = (
            self._client_config["project"],
            self._client_config["dataset"],
            self._client_config["table"],
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
        send_limit: int,
        items: Iterable[GeneratedProtocolMessageType],
    ) -> Generator[Iterator[AppendRowsRequest], None, None]:
        """Generate requests

        Args:
            stream (WriteStream): BigQuery write stream
            proto_schema (ProtoSchema): Protobuf model schema
            send_limit (int): Chunking limit
            items (Iterable[GeneratedProtocolMessageType]): Messages to write,
                                                        protobuf model objects

        Yields:
            Generator[Iterator[AppendRowsRequest], None, None]: _description_
        """
        send_count = 0
        messages = types.ProtoRows()
        for item in items:
            messages.serialized_rows.append(item)
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

    def run(
        self, items: Iterable[GeneratedProtocolMessageType], send_limit: int = 10
    ) -> None:
        """Write using producer

        Args:
            items (Iterable[GeneratedProtocolMessageType]): Messages to write,
                                                            protobuf model objects
            send_limit (int): Chunking limit
        """
        if not self.client:
            self.connect()

        PROTO_DESCRIPTOR = descriptor_pb2.DescriptorProto()
        self.model.DESCRIPTOR.CopyToProto(PROTO_DESCRIPTOR)
        PROTO_SCHEMA = ProtoSchema(proto_descriptor=PROTO_DESCRIPTOR)

        stream = self.create_stream()
        request_generator = self._generate_requests(
            stream=stream,
            proto_schema=PROTO_SCHEMA,
            send_limit=send_limit,
            items=items,
        )

        for resp in self.client.append_rows(requests=request_generator):
            log.debug(resp)
