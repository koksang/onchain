"""Main module"""

from pydoc import importfile
import hydra
from omegaconf import DictConfig, OmegaConf
from onchain.core.logger import log
from onchain.utils.helpers import get_service
from onchain.constants import CONFIG_PATH, CONFIG_NAME


@hydra.main(version_base=None, config_path=CONFIG_PATH, config_name=CONFIG_NAME)
def main(cfg: DictConfig) -> None:
    """Main function to kickstart any service

    Args:
        conf (DictConfig): Parsed config that comes from hydra config_name
    """
    log.debug(OmegaConf.to_yaml(cfg))

    # NOTE: retrieving configs
    resolved_config: dict = OmegaConf.to_container(cfg, resolve=True)
    service = resolved_config["service"]
    runtime_kwargs = resolved_config.pop("runtime")

    # NOTE: search and import service
    module = get_service(service)
    module = getattr(importfile(module), "App")
    app = module(resolved_config, **runtime_kwargs)

    app.run()


if __name__ == "__main__":
    main()
