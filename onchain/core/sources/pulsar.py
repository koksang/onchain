"""Pulsar source"""

from typing import Iterator
import pulsar
from _pulsar import ConsumerType
from google.protobuf.pyext.cpp_message import GeneratedProtocolMessageType
from onchain.core.base import BaseConnectionModule
from onchain.models.mode import ExecutionMode
from onchain.utils.pulsar import get_pulsar_schema
from onchain.logger import log


class PulsarSource(BaseConnectionModule):
    execution_mode = [ExecutionMode.stream]

    def __init__(
        self,
        client_config: dict,
        consumer_config: dict,
        blockchain_name: str,
        blockchain_data: str,
        **kwargs,
    ) -> None:
        """Init

        Args:
            client_config (dict): Pulsar client configuration.
            consumer_config (dict): Pulsar consumer configuration.
            blockchain_name (str): Blockchain name.
            blockchain_data (str): Blockchain data.
        """
        self._client_config = client_config
        self._consumer_config = consumer_config
        super().__init__(blockchain_name, blockchain_data)

    def connect(self, reconnect: bool = False) -> None:
        """Establish client connection

        Args:
            reconnect (bool, optional): To reconnect the client?. Defaults to False.
        """
        if not (self.client and reconnect) or reconnect:
            self.client = pulsar.Client(**self._client_config)
            log.info("Connected to pulsar client")

    def run(self) -> Iterator[GeneratedProtocolMessageType]:
        """Run consumer"""
        self.running = True
        if not self.client:
            self.connect()

        consumer_type = self._consumer_config.get(
            "consumer_type", "shared"
        ).capitalize()
        self._consumer_config["consumer_type"] = getattr(ConsumerType, consumer_type)
        schema = get_pulsar_schema(self.model)
        consumer = self.client.subscribe(**self._consumer_config, schema=schema)

        progress = 0
        while self.running:
            message = consumer.receive()
            try:
                consumer.acknowledge(message)
                progress += 1
                data, id = message.data().decode("utf-8"), message.message_id()
                log.debug(f"Received message '{data}', id={id}")
                yield data
            except Exception:
                self.running = False
                consumer.negative_acknowledge(message)

        self.client.close()
        log.info(f"Consumed {progress} messages.")
