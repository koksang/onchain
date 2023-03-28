"""Collection of blockchain config validators"""

from pydantic.typing import Literal
from pydantic import BaseModel


class EVM(BaseModel):
    coin: Literal[
        "ethereum",
        "polygon",
        "bnb",
    ]
    data: Literal[
        "block",
        "transaction",
        "log",
        "Receipt",
        "Trace",
    ]
    client: dict
    pymodel: Literal["evm"] | None = "evm"


class Cardano(BaseModel):
    coin: Literal["ada"]
    data: Literal["block"]
    client: dict
    pymodel: Literal["cardano"] | None = "cardano"
