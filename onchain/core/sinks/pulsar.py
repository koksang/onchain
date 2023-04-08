"""Pulsar Sink"""

from typing import Iterable
import pulsar
from onchain.core.base import BaseConnectionModule
from onchain.models.mode import ExecutionMode
from onchain.utils.pulsar import get_pulsar_schema
from onchain.logger import log


class PulsarSink(BaseConnectionModule):
    execution_mode = [ExecutionMode.stream]

    def __init__(
        self,
        client_config: dict,
        producer_config: dict,
        blockchain_name: str,
        blockchain_data: str,
        **kwargs,
    ) -> None:
        """Init

        Args:
            client_config (dict): Pulsar client configuration.
            producer_config (dict): Pulsar producer configuration.
            blockchain_name (str): Blockchain name.
            blockchain_data (str): Blockchain data.
        """
        self._client_config = client_config
        self._producer_config = producer_config
        super().__init__(blockchain_name, blockchain_data)

    def connect(self, reconnect: bool = False) -> None:
        """Establish client connection

        Args:
            reconnect (bool, optional): To reconnect the client?. Defaults to False.
        """
        if not (self.client and reconnect) or reconnect:
            self.client = pulsar.Client(**self._client_config)
            log.info("Connected to pulsar client")

    def run(self, upstream_items: Iterable) -> None:
        """Run producer

        Args:
            upstream_items (Iterable): Upstream items

        Returns:
            GeneratedProtocolMessageType: Protobuf model object
        """

        def callback(response, message_id):
            log.debug(f"Message published: {response}, id: {message_id}")

        if not self.client:
            self.connect()

        schema = get_pulsar_schema(self.model)
        producer = self.client.create_producer(**self._producer_config, schema=schema)

        progress = 0
        for item in upstream_items:
            producer.send_async(item, callback)
            progress += 1

        self.client.close()
        log.info(f"Produced {progress} messages.")
