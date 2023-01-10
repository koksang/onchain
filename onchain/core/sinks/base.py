"""Base sink"""
from abc import abstractmethod
from onchain.core.base import BaseModule


class BaseSink(BaseModule):
    @abstractmethod
    def connect(self) -> object:
        pass

    @abstractmethod
    def write(self) -> None:
        pass
