"""Pulsar Sink"""

from typing import Iterable, Union
import pulsar
from onchain.core.sinks.base import BaseSink
from onchain.models.mode import ExecutionMode
from onchain.core.logger import log

DEFAULT_PULSAR_PROXY_IP = "pulsar://localhost:6650"


class PulsarSink(BaseSink):
    execution_mode = [ExecutionMode.stream]

    def __init__(self, config: dict) -> None:
        """Init

        Args:
            config (dict): PULSAR configuration.
        """
        self.config = config
        self.client = None
        log.info(f"Initiated {self._name} with config: {self.config}")

    def connect(self, reconnect: bool = False) -> None:
        """Establish client connection

        Args:
            reconnect (bool, optional): To reconnect the client?. Defaults to False.
        """
        client_config = self.config["client"]
        if not (self.client and reconnect) or reconnect:
            self.client = pulsar.Client(**client_config)
            log.info(f"Connected to pulsar client: {client_config}")

    def write(self, items: Union[Iterable[str], list[str]]) -> None:
        """Write using producer

        Args:
            items (Union[Iterable[str], list[str]]): Messages to write
        """

        def callback(response, message_id):
            log.debug(f"Message published: {response}")

        if not self.client:
            self.connect()

        producer_config = self.config["producer"]
        progress = 0
        producer = self.client.create_producer(producer_config)
        for item in items:
            producer.send_async(item.encode("utf-8"), callback)
            progress += 1

        self.client.close()
        log.info(f"Produced {progress} messages.")
