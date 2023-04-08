"""Base module"""
from abc import ABC, abstractmethod
from onchain.utils.protobuf import get_protobuf_model
from onchain.logger import log


class BaseModule(ABC):
    execution_mode = []

    def __init__(self, blockchain_name: str, blockchain_data: str, **kwargs) -> None:
        self.blockchain_name = blockchain_name
        self.blockchain_data = blockchain_data
        self.model = get_protobuf_model(self.blockchain_name, self.blockchain_data)
        log.info(
            f"Initiated {self._name}, blockhain: {self.blockchain_name}, data: {self.blockchain_data}, model: {self.model}"
        )

    @property
    def _name(self):
        return self.__class__.__name__

    @abstractmethod
    def run(self):
        pass


class BaseConnectionModule(BaseModule):
    client = None
    running = None

    @abstractmethod
    def connect(self):
        pass


class BaseService(BaseModule):
    @property
    def _name(self):
        return self.__class__.__module__

    @abstractmethod
    def run(self) -> None:
        """Run worker"""
        pass
