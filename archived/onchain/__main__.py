"""Main module"""

from pathlib import Path
from typing import Type, Union

import hydra
from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig, OmegaConf

from onchain.constants import CONFIG_NAME, CONFIG_PATH, SERVICES_PATH
from onchain.logger import log
from onchain.validators import Config


def get_service_module(
    config: dict | DictConfig,
    service_name: str | None = None,
    module_name: str | None = "App",
    services_path: str | None = SERVICES_PATH,
) -> type:
    """Search service module from `services` folder

    Args:
        config (Union[dict, DictConfig]): Resolved hydra config
        service_name (Union[str, None], optional): Service name to use if none is specified
                                                    in config. Defaults to None.
        module_name (Union[str, None], optional): Module name to import from service.
                                                    Defaults to "App".
        servicees_path (Union[str, None], optional): Services path. Defaults to SERVICES_PATH

    Returns:
        Type: Imported module
    """
    from pydoc import importfile

    blockchain = config.blockchain.__class__.__name__.lower()
    service_name = config.service or service_name
    service_group_path = Path(services_path, blockchain)
    service = [
        path.absolute() for path in service_group_path.rglob(f"{service_name}.py")
    ]
    log.debug(f"Found service: {service}")
    assert (
        len(service) == 1
    ), f"Found >1 module in path: {service_group_path} with keywords: {service_name}"
    service = service[0]
    log.info(f"Initiating service: {blockchain}.{service.stem}")
    return getattr(importfile(str(service)), module_name)


@hydra.main(version_base=None, config_path=CONFIG_PATH, config_name=CONFIG_NAME)
def main(config: DictConfig) -> None:
    """Main function to kickstart any service

    Args:
        config (DictConfig): Parsed config that comes from hydra config_name
    """
    log.debug(OmegaConf.to_yaml(config))
    choices = HydraConfig.get().runtime.choices
    default_service = f"{choices.source}__{choices.sink}"

    # NOTE: resolving configs
    resolved_config: dict = OmegaConf.to_container(config, resolve=True)
    resolved_config = Config(**resolved_config)

    # NOTE: import and run service
    module = get_service_module(resolved_config, default_service)
    app = module(resolved_config)
    app.run()


if __name__ == "__main__":
    main()
