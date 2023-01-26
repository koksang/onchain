"""Web3 API source"""

# TODO: Replace web3 with requests

from typing import Iterator, Callable
from web3 import Web3
from web3.middleware import geth_poa_middleware
from onchain.core.base import BaseSource
from onchain.models.mode import ExecutionMode
from onchain.core.logger import log


class APISource(BaseSource):
    execution_mode = [ExecutionMode.stream]

    def __init__(self, config: dict, func: Callable) -> None:
        """Init

        Args:
            config (dict): API config
            func (Callable): Defined function
        """
        self.config = config
        self.client = None
        self.running = None
        self.func = func
        log.info(f"Initiated {self._name} with config: {self.config}")

    def connect(self, reconnect: bool = False) -> None:
        """Establish client connection

        Args:
            reconnect (bool, optional): To reconnect the client?. Defaults to False.
        """
        client_config = self.config["client"]
        if not (self.client and reconnect) or reconnect:
            self.client = Web3(Web3.HTTPProvider(**client_config))
            self.client.middleware_onion.inject(geth_poa_middleware, layer=0)
            assert (
                self.client.isConnected()
            ), f"Failed to connect to web3 client: {client_config}"
            log.info(f"Connected to web3 client: {client_config}")

    def read(self) -> Iterator[str]:
        """Read with function using Web3 client

        Args:
            send_limit (int): Limit to chunk the outputs

        Yields:
            Iterator[str]: API outputs
        """
        self.running = True
        if not self.client:
            self.connect()

        assert self.client.isConnected(), "Please connect Web3 client."

        for output in self.func(self):
            yield output
