"""Service with Pulsar source, Bigquery sink"""

from onchain.core.base import BaseService
from onchain.core.sources.pulsar import PulsarSource
from onchain.core.sinks.bigquery import BigQuerySink
from onchain.core.mappers.evm import EVMMapper
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
        # Retrieve configs
        source_config = self.config["source"]
        sink_config = self.config["sink"]
        mapper_config = self.config["mapper"]
        worker_config = self.config["worker"]

        # Initialize objects
        source = PulsarSource(source_config)
        mapper = EVMMapper(mapper_config)
        sink = BigQuerySink(sink_config, mapper=mapper)

        # Run worker
        manager = RayManager(
            config=worker_config,
            source=source,
            sink=sink,
        )
        manager.run()
