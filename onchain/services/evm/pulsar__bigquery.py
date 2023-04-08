"""Service with Pulsar source, Bigquery sink"""

from onchain.core.base import BaseService
from onchain.core.sources.pulsar import PulsarSource
from onchain.core.sinks.bigquery import BigQuerySink
from onchain.core.workers.ray import RayManager
from onchain.logger import log


class App(BaseService):
    def __init__(
        self,
        source_config: dict,
        sink_config: dict,
        worker_config: dict,
        blockchain_config: dict,
        **kwargs,
    ) -> None:
        """Init

        Args:
            source_config (dict): Config for source
            sink_config (dict): Config for sink
            worker_config (dict): Config for worker
            blockchain_config (dict): Config for blockchain
        """
        self._source_config = source_config
        self._sink_config = sink_config
        self._worker_config = worker_config
        self._blockchain_config = blockchain_config
        super().__init__(
            blockchain_name=self._blockchain_config["blockchain_name"],
            blockchain_data=self._blockchain_config["blockchain_data"],
        )

    def run(self):
        """Run service"""

        # Initialize objects
        source = PulsarSource(
            client_config=self._source_config["client"],
            consumer_config=self._source_config["consumer"],
            blockchain_name=self.blockchain_name,
            blockchain_data=self.blockchain_data,
        )
        sink = BigQuerySink(
            client_config=self._sink_config["client"],
            blockchain_name=self.blockchain_name,
            blockchain_data=self.blockchain_data,
        )

        def process():
            return sink.run(source.run())

        # Run worker
        manager = RayManager(config=self._worker_config, process=process)
        manager.run()
