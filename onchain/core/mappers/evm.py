"""Mapper for EVM blockchain data"""

from typing import Union
import json
from importlib import import_module
from google.protobuf.json_format import MessageToDict
from web3.datastructures import AttributeDict
from onchain.core.base import BaseMapper
from onchain.core.logger import log
from onchain.constants import BASE_PATH_PROTO_PYMODEL


class EVMMapper(BaseMapper):
    def __init__(self, model: str, pymodel: str = "evm_pb2", **kwargs) -> None:
        """Init

        Args:
            model (str): _description_
            proto_pymodel (str, optional): _description_. Defaults to "evm_pb2".
        """
        path_to_proto_pymodel = f"{BASE_PATH_PROTO_PYMODEL}.{pymodel}"
        self.model = getattr(import_module(path_to_proto_pymodel), model.capitalize())

    def get_parameters(self) -> list[str]:
        """Get available fields corresponding to protobuf model

        Returns:
            list[str]: List of available fields
        """
        params = [item.name for item in self.model.DESCRIPTOR.fields]
        log.info(f"Retrieved parameters: {params}")
        return params

    def to_proto(self, message: Union[dict, str]) -> object:
        """Convert from json dictionary to protobuf python model

        Args:
            message (dict): JSON dict or str

        Returns:
            object: Converted protobuf model object
        """
        json_dict = json.loads(message) if isinstance(message, str) else message
        item = self.model(**json_dict)
        log.debug(f"Converted to {item}")
        return item

    def to_json(self, message: object) -> dict:
        """Convert from protobuf model to json dictionary

        Args:
            message (object): Protobuf model object

        Returns:
            dict: Converted json dictionary
        """
        item = MessageToDict(message)
        log.debug(f"Converted to {item}")
        return item

    @staticmethod
    def block(data: AttributeDict) -> str:
        """Convert EVM block to json dict

        Args:
            data (AttributeDict): Block attribute dict

        Returns:
            str: Converted json dict str
        """
        datamodel = {
            "number": data.number,
            "hash": data.hash.hex(),
            "parent_hash": data.parentHash.hex(),
            "nonce": data.nonce.hex(),
            "sha3_uncles": data.sha3Uncles.hex(),
            "logs_bloom": data.logsBloom.hex(),
            "transactions_root": data.transactionsRoot.hex(),
            "state_root": data.stateRoot.hex(),
            "receipts_root": data.receiptsRoot.hex(),
            "miner": data.miner,
            "difficulty": data.difficulty,
            "total_difficulty": data.totalDifficulty,
            "extra_data": data.get("extraData", None),
            "size": data.size,
            "gas_limit": data.gasLimit,
            "gas_used": data.gasUsed,
            "base_fee_per_gas": data.get("baseFeePerGas", None),
            "timestamp": data.timestamp,
            "transactions": list(map(lambda item: item.hex(), data.transactions)),
            "uncles": list(map(lambda item: item.hex(), data.uncles)),
        }
        # TODO: convert to protobuf schema later
        return json.dumps(datamodel)

    @staticmethod
    def transaction(data: AttributeDict) -> str:
        """Convert EVM transaction to json dict

        Args:
            data (AttributeDict): Transaction attribute dict

        Returns:
            str: Converted json dict str
        """
        datamodel = {
            "block_hash": data.blockHash.hex(),
            "block_number": data.blockNumber,
            "from": data["from"],
            "gas": data.gas,
            "gas_price": data.gasPrice,
            "hash": data.hash.hex(),
            "input": data.input,
            "nonce": data.nonce.hex(),
            "to": data.to,
            "transaction_index": data.transactionIndex,
            "value": data.value,
            "v": data.v,
            "r": data.r.hex(),
            "s": data.s.hex(),
        }
        return json.dumps(datamodel)
