"""Pulsar helper functions"""

from google.protobuf.descriptor_pb2 import DescriptorProto
from google.protobuf.pyext.cpp_message import GeneratedProtocolMessageType
from onchain.core.schema import ProtobufBytesSchema


def get_pulsar_schema(proto_model: GeneratedProtocolMessageType) -> ProtobufBytesSchema:
    """Get pulsar bytes schema from protobuf model

    Args:
        proto_model (GeneratedProtocolMessageType): Protobuf model object

    Returns:
        ProtobufBytesSchema: Pulsar schema
    """
    protobuf_descriptor = DescriptorProto()
    proto_model.DESCRIPTOR.CopyToProto(protobuf_descriptor)
    return ProtobufBytesSchema(
        record_cls=proto_model, schema_definition=protobuf_descriptor
    )
