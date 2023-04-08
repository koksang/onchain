"""Ray Stream Worker"""

import ray
from typing import Union, Type, Callable
from onchain.core.base import BaseModule
from onchain.logger import log


@ray.remote(num_cpus=0.5)
class RayStreamer(BaseModule):
    def __init__(self, process: Callable, **kwargs) -> None:
        """Init

        Args:
            process (Callable): Process to send to ray workers
        """
        self.process = process
        log.info(f"Initiated {self._name}")

    def run(self) -> None:
        """Run worker"""
        self.process()


class RayManager(BaseModule):
    def __init__(
        self,
        config: dict,
        process: Callable,
        **kwargs,
    ) -> None:
        """Init

        Args:
            config (dict): Ray Manager config
            process (Callable): Process to send to ray workers
        """
        self.config = config
        self.process = process
        log.info(f"Initiated {self._name}")

    def run(
        self, ray_worker: Union[Type[BaseModule], RayStreamer] = RayStreamer
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
                ray_worker.options(**options_config).remote(process=self.process)
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
