#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from typing import Union
import _pulsar
from pulsar.schema import Schema
from google.protobuf.descriptor_pb2 import DescriptorProto
from google.protobuf.json_format import MessageToDict


class ProtobufBytesSchema(Schema):
    def __init__(
        self,
        record_cls: type,
        schema_definition: Union[DescriptorProto, dict, None] = None,
    ) -> None:
        """Initialization function

        Args:
            record_cls (type): Record class, normally this is Protobuf Message class
            schema_definition (Union[DescriptorProto, dict, None]): Protobuf message descriptor
        """
        if isinstance(schema_definition, DescriptorProto):
            schema_definition = MessageToDict(schema_definition)

        super(ProtobufBytesSchema, self).__init__(
            record_cls,
            _pulsar.SchemaType.BYTES,
            schema_definition,
            "PROTOBUF_BYTES",
        )

    def encode(self, obj: type) -> bytes:
        """Encode dict object to Protobuf serialized string

        Args:
            obj (type): Message object

        Returns:
            bytes: Protobuf schema serialized string
        """
        self._validate_object_type(obj)
        return obj.SerializeToString()

    def decode(self, data: bytes) -> type:
        """Decode serialized string to Protobuf object

        Args:
            data (bytes): Serialized string

        Returns:
            type: Protobuf object
        """
        return self._record_cls.FromString(data)

    def __str__(self):
        return self.self.__class__.__name__
