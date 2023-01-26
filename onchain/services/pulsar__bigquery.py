"""Service with Pulsar source, Bigquery sink"""

from onchain.core.base import BaseService
from onchain.core.sources.pulsar import PulsarSource
from onchain.core.sinks.bigquery import BigQuerySink
from onchain.core.methods.evm import APIMethod
from onchain.core.workers.ray import RayManager, RayStreamer
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
        mapper_config = self.config["mapper"]
        worker_config = self.config["worker"]

        # Initialize objects
        source = PulsarSource(source_config)
        sink = BigQuerySink(sink_config, mapper=mapper_config)
        api: APIMethod = APIMethod(method_config)

        # Run worker
        manager = RayManager(config=worker_config, source=source, sink=sink, method=api)
        manager.run(RayStreamer)
