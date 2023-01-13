"""Service with Pulsar source, BigQuery sink"""

from onchain.core.base import BaseService
from onchain.core.mappers.proto import Mapper
from onchain.core.sources.pulsar import PulsarSource
from onchain.core.sinks.bigquery import BigQuerySink
from onchain.core.workers.ray_streamer import RayStreamer


class App(BaseService):
    def __init__(self, config: dict) -> None:
        """Init

        Args:
            config (dict): _description_
        """
        self.source_config = config.get("source")
        self.sink_config = config.get("sink")
        self.mapper_config = config.get("mapper", None)

    def run(self):
        """Run service"""
        mapper = Mapper(**self.mapper_config)
        source = PulsarSource(self.source_config)
        sink = BigQuerySink(self.sink_config, mapper=mapper)
        runner = RayStreamer(source=source, sink=sink)

        runner.run()
