"""Helper functions"""

import json
import pytz
from base64 import b64decode
from typing import Union, Type
from pathlib import Path
from datetime import datetime, timezone
from onchain.logger import log
from onchain.constants import SERVICES_PATH


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


def get_service(config: dict) -> str:
    """Get module file from path

    Args:
        config (dict): Service config

    Returns:
        str: Filtered module absolute path
    """
    source, sink = config["source"], config["sink"]
    path = Path(SERVICES_PATH)
    search_module = f"*{source}__{sink}.py"
    module = [path.absolute() for path in path.rglob(search_module)]
    log.debug(f"Found service: {module}")
    assert (
        len(module) == 1
    ), f"Found >1 module in path: {str(path)} with keywords: {search_module}"
    module = module[0]
    log.info(f"Initiating service: {module.stem}")
    return str(module)


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
