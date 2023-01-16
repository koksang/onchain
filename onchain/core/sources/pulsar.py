"""Pulsar source"""

from typing import Iterator
import pulsar
from onchain.core.base import BaseSource
from onchain.models.mode import ExecutionMode
from onchain.core.logger import log

DEFAULT_PULSAR_PROXY_IP = "pulsar://localhost:6650"

# import logging

# loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]

# print(loggers)
# print(logging.root.manager.loggerDict)
# input("--wait--")


class PulsarSource(BaseSource):
    execution_mode = [ExecutionMode.stream]

    def __init__(self, config: dict) -> None:
        """Init

        Args:
            config (dict): PULSAR configuration.
        """
        self.config = config
        self.client = None
        self.running = None
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

    def read(self) -> Iterator[str]:
        """Read from consumer"""
        self.running = True
        if not self.client:
            self.connect()

        consumer_config = self.config["consumer"]
        progress = 0
        consumer = self.client.subscribe(**consumer_config)

        while self.running:
            message = consumer.receive()
            try:
                consumer.acknowledge(message)
                progress += 1
                data, id = message.data().decode("utf-8"), message.message_id()
                log.debug(f"Received message '{data}' id='{id}'")
                yield data
            except:
                self.running = False
                consumer.negative_acknowledge(message)

        self.client.close()
        log.info(f"Consumed {progress} messages.")
