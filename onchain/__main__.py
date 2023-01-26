"""Main module"""

from pydoc import importfile
import hydra
from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig, OmegaConf
from onchain.core.logger import log
from onchain.utils.helpers import get_service, process_hydra_config
from onchain.constants import CONFIG_PATH, CONFIG_NAME


@hydra.main(version_base=None, config_path=CONFIG_PATH, config_name=CONFIG_NAME)
def main(cfg: DictConfig) -> None:
    """Main function to kickstart any service

    Args:
        conf (DictConfig): Parsed config that comes from hydra config_name
    """
    log.debug(OmegaConf.to_yaml(cfg))
    hydra_choices = HydraConfig.get().runtime.choices

    # NOTE: retrieving configs
    resolved_config: dict = OmegaConf.to_container(cfg, resolve=True)
    resolved_config = process_hydra_config(resolved_config, hydra_choices.keys())

    # NOTE: search and import service
    module = get_service(hydra_choices)
    module = getattr(importfile(module), "App")
    app = module(resolved_config)

    # run service
    app.run()


if __name__ == "__main__":
    main()
