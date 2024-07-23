"""Protobuf helper functions"""

from importlib import import_module
from google.protobuf.pyext.cpp_message import GeneratedProtocolMessageType
from onchain.constants import BASE_PATH_PROTO_PYMODEL
from onchain.logger import log


def get_protobuf_model(
    blockchain_name: str,
    blockchain_data: str,
    protobuf_models_path: str = BASE_PATH_PROTO_PYMODEL,
) -> GeneratedProtocolMessageType:
    """Get protobuf model from blockchain name & data

    Args:
        blockchain_name (str): Blockchain name
        blockchain_data (str): Blockchain data
        protobuf_models_path (str, optional): Protobuf models base path. Defaults to BASE_PATH_PROTO_PYMODEL.

    Returns:
        GeneratedProtocolMessageType: Protobuf model object
    """
    blockchain_name = blockchain_name.strip("_pb2")
    path_to_proto_pymodel = f"{protobuf_models_path}.{blockchain_name}_pb2"
    protobuf_model = getattr(
        import_module(path_to_proto_pymodel), blockchain_data.capitalize()
    )
    log.info(f"Imported {protobuf_model} from {path_to_proto_pymodel}")
    return protobuf_model
