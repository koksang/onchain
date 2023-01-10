"""Pulsar source"""

from typing import Iterable, Union
import pulsar
from onchain.core.sources.base import BaseSource
from onchain.models.mode import ExecutionMode
from onchain.core.logger import log

DEFAULT_PULSAR_PROXY_IP = "pulsar:://localhost:6650"


class PulsarSource(BaseSource):
    execution_mode = [ExecutionMode.stream]

    def __init__(
        self,
        client_config: dict,
        consumer_config: dict,
    ) -> None:
        """Init

        Args:
            client_config (dict): PULSAR Client configuration.
            consumer_config (str): PULSAR consumer configuration.
        """
        self.client_config = client_config
        self.consumer_config = consumer_config
        self.client = None
        log.info(
            f"Initiated {self._name} with client; {self.client_config}, consumer: {self.consumer_config}"
        )

    def connect(self, reconnect: bool = False, **connection_config: dict) -> None:
        """Establish client connection

        Args:
            reconnect (bool, optional): whether to reconnect the client?. Defaults to False.

        Returns:
            pulsar.Client: Pulsar client object
        """
        if not (self.client and reconnect) or reconnect:
            self.client = pulsar.Client(**self.client_config)
            log.info(f"Connected to pulsar client: {self.client_config}")

    def read(self, items: Union[Iterable[str], list[str]]) -> None:
        if not self.client:
            self.connect()

        progress = 0
        consumer = self.client.subsribe(self.consumer_config)

        
