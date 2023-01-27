"""Mapper for EVM blockchain data"""

import json
from web3.datastructures import AttributeDict


class EVMMapper:
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
