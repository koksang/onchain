"""Web3 API source - EVM RPC Methods"""

# TODO: Replace web3 with requests
# TODO: Only fully build this once converted everything into plain API calls
# WIP

from typing import Iterable, Union
from web3 import Web3
from web3.middleware.geth_poa import geth_poa_middleware
from web3.datastructures import AttributeDict
from google.protobuf.pyext.cpp_message import GeneratedProtocolMessageType
from onchain.core.base import BaseConnectionModule
from onchain.models.blockchains.evm_pb2 import (
    Block,
    Transaction,
    Log,
    Receipt,
    Trace,
)
from onchain.models.mode import ExecutionMode
from onchain.logger import log


class EVMAPIMethod(BaseConnectionModule):
    execution_mode = [ExecutionMode.stream]

    def __init__(
        self,
        client_config: dict,
        blockchain_name: str,
        blockchain_data: str,
        **kwargs,
    ) -> None:
        """Init

        Args:
            client_config (dict): Web3 client configuration.
            blockchain_name (str): Blockchain name.
            blockchain_data (str): Blockchain data.
        """
        self._client_config = client_config
        super().__init__(blockchain_name, blockchain_data)

    def connect(self, reconnect: bool = False):
        """Establish client connection

        Args:
            reconnect (bool, optional): To reconnect the client?. Defaults to False.
        """
        if not (self.client and reconnect) or reconnect:
            self.client = Web3(Web3.HTTPProvider(**self._client_config))
            self.client.middleware_onion.inject(geth_poa_middleware, layer=0)
            assert (
                self.client.isConnected()
            ), f"Failed to connect to web3 client: {self._client_config}"
            log.info("Connected to web3 client")

    def block(self, input: Union[str, int]) -> GeneratedProtocolMessageType:
        """Get block

        Args:
            input (Union[str, int]): Input

        Returns:
            GeneratedProtocolMessageType: Protobuf model object
        """
        data: AttributeDict = self.client.eth.get_block(input)
        return Block(
            number=data.number,
            hash=data.hash.hex(),
            parent_hash=data.parentHash.hex(),
            nonce=data.nonce.hex(),
            sha3_uncles=data.sha3Uncles.hex(),
            logs_bloom=data.logsBloom.hex(),
            transactions_root=data.transactionsRoot.hex(),
            state_root=data.stateRoot.hex(),
            receipts_root=data.receiptsRoot.hex(),
            miner=data.miner,
            difficulty=data.difficulty,
            total_difficulty=data.totalDifficulty,
            extra_data=data.get("extraData", None),
            size=data.size,
            gas_limit=data.gasLimit,
            gas_used=data.gasUsed,
            base_fee_per_gas=data.get("baseFeePerGas", None),
            timestamp=data.timestamp,
            transactions=list(map(lambda item: item.hex(), data.transactions)),
            uncles=list(map(lambda item: item.hex(), data.uncles)),
        )

    def transaction(self, input: Union[str, int]) -> GeneratedProtocolMessageType:
        """Get transaction

        Args:
            input (Union[str, int]): Input

        Returns:
            GeneratedProtocolMessageType: Protobuf model object
        """
        data: AttributeDict = self.client.eth.get_block(input)
        item = Transaction(
            block_hash=data.blockHash.hex(),
            block_number=data.blockNumber,
            gas=data.gas,
            gas_price=data.gasPrice,
            hash=data.hash.hex(),
            input=data.input,
            nonce=data.nonce.hex(),
            to=data.to,
            transaction_index=data.transactionIndex,
            value=data.value,
            v=data.v,
            r=data.r.hex(),
            s=data.s.hex(),
        )
        setattr(item, "from", data["from"])
        return item

    def run(self, upstream_items: Iterable) -> Iterable[GeneratedProtocolMessageType]:
        """Run method

        Args:
            upstream (Iterable): Upstream module

        Returns:
            GeneratedProtocolMessageType: Protobuf model object
        """
        if not self.client:
            self.connect()

        function = getattr(self, self.blockchain_data)
        log.info(f"Retrieved API method: {function.__name__}")

        for item in upstream_items:
            yield function(item)
