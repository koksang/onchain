"""Builder for models"""

from typing import Union
import json
from importlib import import_module
from google.protobuf.json_format import MessageToDict
from onchain.core.logger import log
from onchain.constants import BASE_PATH_PROTO_PYMODEL


class ProtoBuilder:
    def __init__(self, model: str, pymodel: str = "evm_pb2", **kwargs) -> None:
        """Init

        Args:
            model (str): _description_
            proto_pymodel (str, optional): _description_. Defaults to "evm_pb2".
        """
        path_to_proto_pymodel = f"{BASE_PATH_PROTO_PYMODEL}.{pymodel}"
        self.model = getattr(import_module(path_to_proto_pymodel), model.capitalize())

    def get_parameters(self) -> list[str]:
        """Get available fields corresponding to protobuf model

        Returns:
            list[str]: List of available fields
        """
        params = [item.name for item in self.model.DESCRIPTOR.fields]
        log.info(f"Retrieved parameters: {params}")
        return params

    def to_proto(self, message: Union[dict, str]) -> object:
        """Convert from json dictionary to protobuf python model

        Args:
            message (dict): JSON dict or str

        Returns:
            object: Converted protobuf model object
        """
        json_dict = json.loads(message) if isinstance(message, str) else message
        item = self.model(**json_dict)
        log.debug(f"Converted to {item}")
        return item

    def to_json(self, message: object) -> dict:
        """Convert from protobuf model to json dictionary

        Args:
            message (object): Protobuf model object

        Returns:
            dict: Converted json dictionary
        """
        item = MessageToDict(message)
        log.debug(f"Converted to {item}")
        return item
