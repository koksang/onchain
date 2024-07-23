"""Main module"""

import logging as log

import hydra
from omegaconf import DictConfig, OmegaConf

from onchain.utils.helpers import setup_logging


@hydra.main(version_base=None, config_path="../conf", config_name="main")
def main(config: DictConfig) -> None:
    """Main function

    Args:
        config (DictConfig): Parsed config that comes from hydra config_name
    """
    conf: dict = OmegaConf.to_container(config, resolve=True)
    setup_logging(log_config=conf["log"])
    log.debug(f"Run config: {conf}")


if __name__ == "__main__":
    main()
