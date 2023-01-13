"""Base workeer"""
from abc import abstractmethod
from onchain.core.base import BaseModule


class BaseWorker(BaseModule):
    @abstractmethod
    def process(self) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass
