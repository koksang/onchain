"""RPC Functions associated with EVM"""

from typing import Iterable, Union
from onchain.core.sources.api import APISource
from onchain.core.mappers.evm import EVMMapper


def get_block(
    instance: APISource, start_block: int, end_block: Union[int, str]
) -> Iterable[dict]:
    """Get block by block number

    Args:
        instance (APISource): EVM source instance
        start_block (int): Start block to retrieve
        end_block (Union[int, str]): End block to retrieve

    Yields:
        dict: Block
    """
    client = instance.client
    if isinstance(end_block, str) and end_block.lower() == "latest":
        data = EVMMapper.block_to_dict(client.eth.get_block(end_block))
        end_block = int(data["number"]) - 1
        yield data

    end_block = int(end_block)
    for block_number in range(start_block, end_block):
        yield EVMMapper.block_to_dict(client.eth.get_block(block_number))
