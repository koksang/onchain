"""Helper functions"""

import json
import pytz
from importlib import import_module
from base64 import b64decode
from typing import Union, Type
from datetime import datetime, timezone
from onchain.constants import BASE_PATH_PROTO_PYMODEL
from onchain.logger import log


def timestamp_to_integer(ts: Union[datetime, str]) -> int:
    """Convert timestamp datetime/ string into integer

    Args:
        ts (Union[datetime, str]): Timestamp value

    Returns:
        int: Converted timestamp integer
    """
    from dateutil.parser import parse

    if isinstance(ts, str):
        ts = parse(ts)

    ts = ts.astimezone(pytz.timezone("utc"))
    delta = ts - datetime(1970, 1, 1, tzinfo=timezone.utc)
    ts_value = int(delta.total_seconds()) * 1000000 + int(delta.microseconds)
    log.debug(f"Converted {ts} to {ts_value}")
    return ts_value


def decode_b64_json_string(encoded: bytes, format: str = "utf-8") -> dict:
    """Decode base64 encoded json string

    Args:
        encoded (bytes): Encoded json string in provided format
        format (str): Encoded format. Defaults to utf-8

    Returns:
        dict: Decoded json string
    """
    return json.loads(b64decode(encoded).decode(format))


def get_class_name(object: Type) -> str:
    """Return object class name

    Args:
        object (Type): Object instance

    Returns:
        str: class name
    """
    return object.__class__.__name__
