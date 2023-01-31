"""Service with Bigquery source, Pulsar sink"""

from onchain.core.base import BaseService
from onchain.core.sources.bigquery import BigQuerySource
from onchain.core.sinks.pulsar import PulsarSink
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
        worker_config = self.config["worker"]

        # Initialize objects
        source = BigQuerySource(source_config)
        sink = PulsarSink(sink_config)

        # Run worker
        manager = RayManager(config=worker_config, source=source, sink=sink)
        manager.run()
