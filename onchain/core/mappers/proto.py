"""Mapper for protobuf models"""

from importlib import import_module
from google.protobuf.json_format import MessageToDict
from onchain.core.logger import log
from onchain.constants import BASE_PATH_PROTO_PYMODEL


class ProtoMapper:
    def __init__(self, proto_pymodel: str, model: str, **kwargs) -> None:
        try:
            path_to_proto_pymodel = f"{BASE_PATH_PROTO_PYMODEL}.{proto_pymodel}"
            self.model = getattr(
                import_module(path_to_proto_pymodel), model.capitalize()
            )
        except ModuleNotFoundError as error:
            log.error(error)

    def get_parameters(self) -> list[str]:
        """Get available fields corresponding to protobuf model

        Returns:
            list[str]: List of available fields
        """
        params = [item.name for item in self.model.DESCRIPTOR.fields]
        log.info(f"Retrieved parameters: {params}")
        return params

    def json_to_proto(self, json_dict: dict) -> object:
        """Convert from json dictionary to protobuf python model

        Args:
            json_dict (dict): JSON dict

        Returns:
            object: Converted protobuf model object
        """
        item = self.model(**json_dict)
        log.debug(f"Converted to {item}")
        return item

    def proto_to_json(self, proto_model: object) -> dict:
        """Convert from protobuf model to json dictionary

        Args:
            proto_model (object): Protobuf model object

        Returns:
            dict: Converted json dictionary
        """
        item = MessageToDict(proto_model)
        log.debug(f"Converted to {item}")
        return item
