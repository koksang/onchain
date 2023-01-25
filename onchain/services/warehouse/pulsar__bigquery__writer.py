"""Service with Pulsar source, BigQuery sink"""

from typing import Union
from onchain.core.base import BaseService
from onchain.core.mappers.proto import ProtoMapper
from onchain.core.sources.pulsar import PulsarSource
from onchain.core.sinks.bigquery import BigQuerySink
from onchain.core.workers.ray import RayStreamer


class App(BaseService):
    def __init__(
        self,
        source_config: dict,
        sink_config: dict,
        mapper_config: Union[dict, None] = None,
        **runtime_kwargs,
    ) -> None:
        """Init

        Args:
            source_config (dict): Config for source
            sink_config (dict): Config for sink
            mapper_config (dict): Config for mapper
        """
        self.source_config = source_config
        self.sink_config = sink_config
        self.mapper_config = mapper_config
        self.runtime_kwargs = runtime_kwargs

    def run(self):
        """Run service"""
        mapper = ProtoMapper(**self.mapper_config)
        source = PulsarSource(self.source_config)
        sink = BigQuerySink(self.sink_config, mapper=mapper)
        runner = RayStreamer(source=source, sink=sink)

        runner.run()
