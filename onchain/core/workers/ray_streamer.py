"""Ray Stream Worker"""

import ray
from onchain.core.workers.base import BaseWorker
from onchain.core.sources.base import BaseSource
from onchain.core.sinks.base import BaseSink
from onchain.models.mode import ExecutionMode


class RayStreamer(BaseWorker):
    def __init__(self, source: BaseSource, sink: BaseSink) -> None:
        self.source = source
        self.sink = sink

    
