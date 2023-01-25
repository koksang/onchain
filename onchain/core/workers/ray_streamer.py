"""Ray Stream Worker"""

import ray
from onchain.core.base import BaseWorker, BaseSource, BaseSink


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

        @ray.remote
        def test():
            pass

        messages = self.source.read()
        self.sink.write(messages)
