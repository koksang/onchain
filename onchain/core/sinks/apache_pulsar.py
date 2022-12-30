"""Pulsar Sink"""

import pulsar
from onchain.core.sinks.base import BaseSink
from onchain.models.mode import ExecutionMode

DEFAULT_PULSAR_PROXY_IP = "pulsar:://localhost:6650"


class PulsarSink(BaseSink):
    def __init__(
        self,
        pulsar_proxy_ip: str = DEFAULT_PULSAR_PROXY_IP,
    ) -> None:
        self.pulsar_proxy_ip = pulsar_proxy_ip
        self.client = None

    def connect(
        self, reconnect: bool = False, **connection_config: dict
    ) -> pulsar.Client:
        """Establish client connection

        Args:
            reconnect (bool, optional): whether to reconnect the client?. Defaults to False.

        Returns:
            pulsar.Client: Pulsar client object
        """
        if not (self.client and reconnect) or reconnect:
            client = pulsar.Client(self.pulsar_proxy_ip, **connection_config)
        return client

    def write(
        self,
        exection_mode: ExecutionMode = ExecutionMode.stream,
    ) -> None:
        # self.client = self.connect()
        pass
