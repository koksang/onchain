"""Pulsar Sink"""

from typing import Iterable, Union
import pulsar
from onchain.core.sinks.base import BaseSink
from onchain.models.mode import ExecutionMode
from onchain.core.logger import log

DEFAULT_PULSAR_PROXY_IP = "pulsar:://localhost:6650"


class PulsarSink(BaseSink):
    execution_mode = [ExecutionMode.stream]

    def __init__(
        self,
        client_config: dict,
        producer_config: dict,
    ) -> None:
        """Init

        Args:
            producer_config (str): PULSAR producer configuration.
            client_config (dict): PULSAR Client configuration.
        """
        self.client_config = client_config
        self.producer_config = producer_config
        self.client = None
        log.info(
            f"Initiated {self._name} with client; {self.client_config}, producer: {self.producer_config}"
        )

    def connect(self, reconnect: bool = False) -> None:
        """Establish client connection

        Args:
            reconnect (bool, optional): whether to reconnect the client?. Defaults to False.

        Returns:
            pulsar.Client: Pulsar client object
        """
        if not (self.client and reconnect) or reconnect:
            self.client = pulsar.Client(**self.client_config)
            log.info(f"Connected to pulsar client: {self.client_config}")

    def write(self, items: Union[Iterable[str], list[str]]) -> None:
        """Write using producer

        Args:
            items (Union[Iterable[str], list[str]]): messages to write
        """

        def callback(response, message_id):
            log.debug(f"Message published: {response}")

        if not self.client:
            self.connect()

        progress = 0
        producer = self.client.create_producer(self.producer_config)
        for item in items:
            producer.send_async(item.encode("utf-8"), callback)
            progress += 1

        self.client.close()
        log.info(f"Produced {progress} messages.")
