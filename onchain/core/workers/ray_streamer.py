"""Ray Stream Worker"""

from onchain.core.workers.base import BaseWorker
from onchain.core.sources.base import BaseSource
from onchain.core.sinks.base import BaseSink


class RayStreamer(BaseWorker):
    def __init__(self, source: BaseSource, sink: BaseSink) -> None:
        """Init

        Args:
            source (BaseSource): Source object
            sink (BaseSink): Sink object
        """
        self.source = source
        self.sink = sink

    def run(self) -> None:
        """Run worker"""
        messages = self.source.read()
        self.sink.write(messages)
