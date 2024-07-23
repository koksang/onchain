"""Helper functions"""

import logging
import logging.config
from pathlib import Path

import yaml


def setup_logging(
    log_config: str | dict = str(Path("conf", "log.yaml")),
    logger_name: str = "onchain",
) -> None:
    """Setup logging

    Args:
        log_config (str | dict, optional): log config filepath. Defaults to "conf/log_config.yaml".
        logger_name (str, optional): logger name. Defaults to "onchain".
    """
    config = (
        yaml.safe_load(open(log_config).read())
        if not isinstance(log_config, dict)
        else log_config
    )
    logging.config.dictConfig(config)
    logging.getLogger(logger_name)
