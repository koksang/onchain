"""Base source"""
from abc import abstractmethod
from onchain.core.base import BaseModule


class BaseSource(BaseModule):
    @abstractmethod
    def connect(self) -> object:
        pass

    @abstractmethod
    def read(self) -> None:
        pass
