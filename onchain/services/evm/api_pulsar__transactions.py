"""Service with Blocks API source, Pulsar sink"""

from onchain.core.base import BaseService
from onchain.core.sources.api import EVMSource
from onchain.core.sinks.pulsar import PulsarSink
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
        source = EVMSource(self.source_config)
        sink = PulsarSink(self.sink_config)
        runner = RayStreamer(source=source, sink=sink)

        runner.run()
