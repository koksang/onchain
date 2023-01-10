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
        self.running = None
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

    def read(self) -> None:
        """Read from consumer"""
        self.running = True
        if not self.client:
            self.connect()

        self.running = True
        progress = 0
        consumer = self.client.subscribe(self.consumer_config)

        while self.running:
            try:
                message = consumer.receive()
                consumer.acknowledge(message)
                progress += 1
                data, id = message.data().decode("utf-8"), message.message_id()
                log.debug(f"Received message '{data}' id='{id}'")
                yield data
            except:
                self.running = False
                consumer.negative_acknowledge(message)
            finally:
                self.running = False

        log.info(f"Consumed {progress} messages.")
