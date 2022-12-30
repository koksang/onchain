"""Base module"""
from abc import ABC, abstractmethod
from onchain.models.mode import ExecutionMode


class BaseModule(ABC):
    supported_modes = []

    @property
    def _name(self):
        return self.__class__.__name__

    @abstractmethod
    def run(self, execution_mode: ExecutionMode) -> None:
        """Run worker"""
        pass
