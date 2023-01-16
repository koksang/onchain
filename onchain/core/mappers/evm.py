"""Mapper for EVM blockchain data"""

import json
from web3.datastructures import AttributeDict


class EVMMapper:
    @staticmethod
    def block_to_dict(data: AttributeDict) -> str:
        """Convert EVM block to json dict

        Args:
            data (AttributeDict): Block attribute dict

        Returns:
            str: Converted json dict str
        """
        datamodel = {
            "number": data.number,
            "hash": data.hash.hex(),
            "parentHash": data.parentHash.hex(),
            "nonce": data.nonce.hex(),
            "sha3Uncles": data.sha3Uncles.hex(),
            "logsBloom": data.logsBloom.hex(),
            "transactionsRoot": data.transactionsRoot.hex(),
            "stateRoot": data.stateRoot.hex(),
            "receiptsRoot": data.receiptsRoot.hex(),
            "miner": data.miner,
            "difficulty": data.difficulty,
            "totalDifficulty": data.totalDifficulty,
            "extraData": data.get("extraData", None),
            "size": data.size,
            "gasLimit": data.gasLimit,
            "gasUsed": data.gasUsed,
            "baseFeePerGas": data.get("baseFeePerGas"),
            "timestamp": data.timestamp,
            "transactions": list(map(lambda item: item.hex(), data.transactions)),
            "uncles": list(map(lambda item: item.hex(), data.uncles)),
        }
        # TODO: convert to protobuf schema later
        return json.dumps(datamodel)

    @staticmethod
    def transaction_to_dict(data: AttributeDict) -> str:
        """Convert EVM transaction to json dict

        Args:
            data (AttributeDict): Transaction attribute dict

        Returns:
            str: Converted json dict str
        """
        datamodel = {
            "blockHash": data.blockHash.hex(),
            "blockNumber": data.blockNumber,
            "from": data["from"],
            "gas": data.gas,
            "gasPrice": data.gasPrice,
            "hash": data.hash.hex(),
            "input": data.input,
            "nonce": data.nonce.hex(),
            "to": data.to,
            "transactionIndex": data.transactionIndex,
            "value": data.value,
            "v": data.v,
            "r": data.r.hex(),
            "s": data.s.hex(),
        }
        return json.dumps(datamodel)
