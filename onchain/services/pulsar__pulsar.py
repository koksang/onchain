"""Service with Blocks API source, Pulsar sink"""

from onchain.core.base import BaseService
from onchain.core.sources.pulsar import PulsarSource
from onchain.core.sinks.pulsar import PulsarSink
from onchain.core.methods.evm import EVMAPIMethod
from onchain.core.workers.ray import RayManager
from onchain.core.logger import log


class App(BaseService):
    def __init__(self, config: dict, **kwargs) -> None:
        """Init

        Args:
            config (dict): Config for source, sink, worker, mapper
        """
        self.config = config
        log.info(f"Initiated service: {self._name}")

    def run(self):
        """Run service"""
        source_config = self.config["source"]
        sink_config = self.config["sink"]
        method_config = self.config["method"]
        worker_config = self.config["worker"]

        # Initialize objects
        source = PulsarSource(source_config)
        sink = PulsarSink(sink_config)
        api = EVMAPIMethod(method_config)

        # Run worker
        manager = RayManager(
            config=worker_config,
            source=source,
            sink=sink,
            method=api,
        )
        manager.run()
