"""Service with Blocks API source, Pulsar sink"""

from functools import partial
from onchain.core.base import BaseService
from onchain.core.sources.api import APISource
from onchain.core.sinks.pulsar import PulsarSink
from onchain.core.workers.ray_streamer import RayStreamer
from onchain.services.evm.functions import get_block
from onchain.core.logger import log


class App(BaseService):
    def __init__(
        self,
        config: dict,
        **runtime_kwargs,
    ) -> None:
        """Init

        Args:
            config (dict): Config for source, sink, worker, mapper
        """
        self.config = config
        self.runtime_kwargs = runtime_kwargs
        log.info(f"Initiated service: {self._name}, runtime: {self.runtime_kwargs}")

    def run(self):
        """Run service"""
        source_config = self.config["source"]
        sink_config = self.config["sink"]
        func = partial(get_block, **self.runtime_kwargs)
        source = APISource(source_config, func=func)
        sink = PulsarSink(sink_config)
        worker = RayStreamer(source=source, sink=sink)
        worker.run()
