"""Ray Stream Worker"""

from typing import Iterable, Union, Type
from onchain.core.base import BaseWorker, BaseSource, BaseSink, BaseMethod


# @ray.remote
class RayStreamer(BaseWorker):
    def __init__(
        self,
        source: Type[BaseSource],
        sink: Type[BaseSink],
        method: Union[Type[BaseMethod], None] = None,
    ) -> None:
        """Init

        Args:
            source (BaseSource): Source object
            sink (BaseSink): Sink object
            method (BaseMethod): Method object. Defaults to None
        """
        self.source = source
        self.sink = sink
        self.method = method

    def run(self) -> None:
        """Run worker"""

        def transform() -> Iterable:
            """Transform source messages with method process"""
            for message in self.source.read():
                yield self.method.process(message)

        messages = self.transform() if self.method else self.source.read()
        self.sink.write(messages)
