"""Service with Blocks API source, Pulsar sink"""

from typing import Iterable
from functools import partial
from onchain.core.base import BaseService
from onchain.core.sources.api import EVMSource
from onchain.core.sinks.pulsar import PulsarSink
from onchain.core.mappers.evm import EVMMapper
from onchain.core.workers.ray_streamer import RayStreamer


def get_block(
    instance: EVMSource,
    block_numbers: tuple[int, str],
) -> Iterable[dict]:
    """Get block by block number

    Args:
        instance (EVMSource): EVM source instance
        block_numbers tuple[int, str]: Blocks to retrieve,
                                in form of (start_block, end_block)

    Yields:
        _type_: Block
    """
    client = instance.client
    start, end = block_numbers
    if isinstance(end, str) and end.lower() == "latest":
        data = EVMMapper.block_to_dict(client.eth.get_block(end))
        end = data["blockNumber"] - 1
        yield data

    start, end = int(start), int(end)
    for block_number in range(start, end):
        yield EVMMapper.block_to_dict(client.eth.get_block(block_number))


class App(BaseService):
    def __init__(self, config: dict, runtime_config: dict) -> None:
        """Init

        Args:
            config (dict): Config for source, sink, worker
            runtime_config (dict): Config for service specific functions
        """
        self.config = config
        self.runtime_config = runtime_config

    def run(self):
        """Run service"""
        block_numbers = self.runtime_config["block_numbers"]
        func = partial(get_block, block_numbers=block_numbers)
        source = EVMSource(self.config["source"], func=func)
        sink = PulsarSink(self.config["sink"])
        worker = RayStreamer(source=source, sink=sink)

        worker.run()
