"""Service with Bigquery source, Pulsar sink"""

from onchain.core.base import BaseService
from onchain.core.sources.bigquery import BigQuerySource
from onchain.core.sinks.pulsar import PulsarSink
from onchain.core.workers.ray import RayManager
from onchain.queries.bigquery import EVMQuery
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
        source = BigQuerySource(
            client_config=self._source_config["client"],
            blockchain_name=self.blockchain_name,
            blockchain_data=self.blockchain_data,
        )
        sink = PulsarSink(
            client_config=self._sink_config["client"],
            producer_config=self._sink_config["producer"],
            blockchain_name=self.blockchain_name,
            blockchain_data=self.blockchain_data,
        )

        def process()
            return sink.run()

        # Run worker
        manager = RayManager(config=worker_config, source=source, sink=sink)
        manager.run()
