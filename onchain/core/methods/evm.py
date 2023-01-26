"""Web3 API source - EVM RPC Methods"""

# TODO: Replace web3 with requests
# TODO: Only fully build this once converted everything into plain API calls
# WIP

from typing import Iterable, Union
from enum import Enum
from web3 import Web3
from web3.middleware.geth_poa import geth_poa_middleware
from web3.datastructures import AttributeDict
from onchain.core.base import BaseMethod
from onchain.models.mode import ExecutionMode
from onchain.core.logger import log


class Method(Enum):
    block = BLOCK = "get_block"
    transaction = TRANSACTION = "get_transaction"


class APIMethod(BaseMethod):
    execution_mode = [ExecutionMode.stream]

    def __init__(self, config: dict) -> None:
        """Init

        Args:
            config (dict): API config
            func (Callable): Defined function
        """
        self.config = config
        self._client, self.func = None, None
        self.connect()
        self.function()
        log.info(f"Initiated {self._name} with config: {self.config}")

    def connect(self, reconnect: bool = False):
        """Establish client connection

        Args:
            reconnect (bool, optional): To reconnect the client?. Defaults to False.
        """
        client_config = self.config["client"]
        if not (self._client and reconnect) or reconnect:
            self._client = Web3(Web3.HTTPProvider(**client_config))
            self._client.middleware_onion.inject(geth_poa_middleware, layer=0)
            assert (
                self._client.isConnected()
            ), f"Failed to connect to web3 client: {client_config}"
            log.info(f"Connected to web3 client: {client_config}")

    def function(self) -> None:
        """Get Web3 function"""
        function_type = getattr(Method, self.config["type"]).value
        log.info(f"Retrieving API function: {function_type}")
        self.func = getattr(self._client.eth, function_type)

    def process(
        self, item: Union[str, int], **kwargs
    ) -> Iterable[Union[dict, AttributeDict]]:
        """Run using Web3 client

        Yields:
            Iterable[Union[dict, AttributeDict]]: API output
        """
        yield self.func(item, **kwargs)
