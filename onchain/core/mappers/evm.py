"""Mapper for EVM blockchain data"""

from web3.datastructures import AttributeDict


class EVMMapper:
    @staticmethod
    def block_to_dict(data: AttributeDict) -> dict:
        """Convert EVM block to json dict

        Args:
            data (AttributeDict): Block attribute dict

        Returns:
            dict: Converted json dict
        """
        data_json = vars(data)
        data_json["proofOfAuthorityData"] = data_json["proofOfAuthorityData"].hex()
        data_json["logsBloom"] = data_json["logsBloom"].hex()
        data_json["miner"] = data_json["miner"].hex()
        data_json["mixHash"] = data_json["mixHash"].hex()
        data_json["nonce"] = data_json["nonce"].hex()
        data_json["parentHash"] = data_json["parentHash"].hex()
        data_json["receiptsRoot"] = data_json["receiptsRoot"].hex()
        data_json["sha3Uncles"] = data_json["sha3Uncles"].hex()
        data_json["stateRoot"] = data_json["stateRoot"].hex()
        data_json["transactions"] = list(
            map(lambda item: item.hex(), data_json["transactions"])
        )
        data_json["transactionsRoot"] = data_json["transactionsRoot"].hex()
        return data_json

    @staticmethod
    def transaction_to_dict(data: AttributeDict) -> dict:
        """Convert EVM transaction to json dict

        Args:
            data (AttributeDict): Transaction attribute dict

        Returns:
            dict: Converted json dict
        """
        data_json = vars(data)
        data_json["blockHash"] = data_json["blockHash"].hex()
        data_json["hash"] = data_json["hash"].hex()
        data_json["r"] = data_json["r"].hex()
        data_json["s"] = data_json["s"].hex()
        return data_json
