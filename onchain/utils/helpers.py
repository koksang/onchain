"""Helper functions"""

import json
import pytz
from base64 import b64decode
from typing import Union
from pathlib import Path
from dateutil.parser import parse
from datetime import datetime, timezone
from onchain.core.logger import log
from onchain.constants import SERVICES_PATH


def timestamp_to_integer(ts: Union[datetime, str]) -> int:
    """Convert timestamp datetime/ string into integer

    Args:
        ts (Union[datetime, str]): Timestamp value

    Returns:
        int: Converted timestamp integer
    """
    if isinstance(ts, str):
        ts = parse(ts)

    ts = ts.astimezone(pytz.timezone("utc"))
    delta = ts - datetime(1970, 1, 1, tzinfo=timezone.utc)
    ts_value = int(delta.total_seconds()) * 1000000 + int(delta.microseconds)
    log.debug(f"Converted {ts} to {ts_value}")
    return ts_value


def get_service(config: dict):
    """Get module file from path

    Args:
        config (dict): Service config

    Returns:
        str: Filtered module absolute path
    """
    group, source, sink = config["group"], config["source"], config["sink"]
    path = Path(SERVICES_PATH, group)
    search_module = f"*{source}__{sink}.py"
    module = [str(path.absolute()) for path in path.rglob(search_module)]
    assert (
        len(module) == 1
    ), f"Found >1 module in path: {str(path)} with keywords: {search_module}"
    module = module[0]
    log.info(f"Found service: {module}.")
    return module


def decode_b64_json_string(encoded: bytes) -> dict:
    """Decode base64 encoded json string

    Args:
        encoded (bytes): Encoded json string, ASCII

    Returns:
        dict: Decoded json string
    """
    return json.loads(b64decode(encoded))
