"""Collection of services setup validators"""

from pydantic.typing import Union
from pydantic import BaseModel
from onchain.validators.blockchain import EVM, Cardano

_SUPPORTED_BLOCKCHAINS = [
    EVM,
    Cardano,
]


class Source(BaseModel):
    client: dict
    consumer: dict | None = None


class Sink(BaseModel):
    client: dict
    producer: dict | None = None


class Worker(BaseModel):
    client: dict
    options: dict
    num_of_actors: int


class Config(BaseModel):
    blockchain: Union[EVM, Cardano]
    source: Source
    sink: Sink
    worker: Worker
    service: str | None = None
