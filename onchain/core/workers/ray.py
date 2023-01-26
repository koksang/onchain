"""Ray Stream Worker"""

import ray
from typing import Iterable, Union, Type
from onchain.core.base import BaseWorker, BaseSource, BaseSink, BaseMethod
from onchain.core.logger import log


@ray.remote(num_cpus=0.5)
class RayStreamer(BaseWorker):
    def __init__(
        self,
        source: Type[BaseSource],
        sink: Type[BaseSink],
        method: Union[Type[BaseMethod], None] = None,
        **kwargs,
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
        log.info(f"Initiated {self._name}")

    def run(self) -> None:
        """Run worker"""

        def transform() -> Iterable:
            """Transform source messages with method process"""
            for message in self.source.read():
                yield self.method.process(message)

        if self.method:
            log.info("Source -> Transform -> Sink")
            messages = self.transform()

        else:
            log.info("Source -> Sink")
            messages = self.source.read()

        self.sink.write(messages)


class RayManager(BaseWorker):
    def __init__(
        self,
        config: dict,
        source: Type[BaseSource],
        sink: Type[BaseSink],
        method: Union[Type[BaseMethod], None] = None,
        **kwargs,
    ) -> None:
        """Init

        Args:
            config (dict): Ray Manager config
            source (BaseSource): Source object
            sink (BaseSink): Sink object
            method (BaseMethod): Method object. Defaults to None
        """
        self.source = source
        self.sink = sink
        self.method = method
        self.config = config
        log.info(f"Initiated {self._name}")

    def run(
        self, ray_worker: Union[Type[BaseWorker], RayStreamer] = RayStreamer
    ) -> None:
        """Run ray manager

        Args:
            ray_worker (Type[BaseWorker]): Ray worker object. Defaults to RayStreamer
        """
        options_config = self.config["options"]
        num_of_actors = self.config["num_of_actors"]
        log.info(f"Creating {num_of_actors} actors")
        try:
            ray.init()
            actors = [
                ray_worker.options(**options_config).remote(
                    source=self.source, sink=self.sink, method=self.method
                )
                for _ in range(num_of_actors)
            ]
            result_ids = [actor.run.remote() for actor in actors]
            while len(result_ids):
                done_ids, result_ids = ray.wait(result_ids)
                log.info(
                    f"Progress - Completed: {len(done_ids)}, Remaining: {len(result_ids)}"
                )
        except Exception as error:
            log.error(error)
        finally:
            ray.shutdown()
