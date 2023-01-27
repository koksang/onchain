"""Base module"""
from abc import ABC, abstractmethod


class BaseModule(ABC):
    supported_modes = []

    @property
    def _name(self):
        return self.__class__.__name__


class BaseSource(BaseModule):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def read(self):
        pass


class BaseSink(BaseModule):
    @abstractmethod
    def connect(self) -> object:
        pass

    @abstractmethod
    def write(self) -> None:
        pass


class BaseWorker(BaseModule):
    @abstractmethod
    def run(self) -> None:
        pass


class BaseMethod(BaseModule):
    @abstractmethod
    def process(self) -> None:
        pass


class BaseBuilder(BaseModule):
    @abstractmethod
    def get_parameters(self) -> None:
        pass

    @abstractmethod
    def to_json(self) -> None:
        pass


class BaseService(ABC):
    @property
    def _name(self):
        return self.__class__.__module__

    @abstractmethod
    def run(self) -> None:
        """Run worker"""
        pass
