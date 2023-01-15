# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: evm.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tevm.proto\"\x82\x03\n\x05\x42lock\x12\x0e\n\x06number\x18\x01 \x01(\x03\x12\x0c\n\x04hash\x18\x02 \x01(\t\x12\x12\n\nparentHash\x18\x03 \x01(\t\x12\r\n\x05nonce\x18\x04 \x01(\t\x12\x12\n\nsha3Uncles\x18\x05 \x01(\t\x12\x11\n\tlogsBloom\x18\x06 \x01(\t\x12\x18\n\x10transactionsRoot\x18\x07 \x01(\t\x12\x11\n\tstateRoot\x18\x08 \x01(\t\x12\x14\n\x0creceiptsRoot\x18\t \x01(\t\x12\r\n\x05miner\x18\n \x01(\t\x12\x12\n\ndifficulty\x18\x0b \x01(\x03\x12\x17\n\x0ftotalDifficulty\x18\x0c \x01(\x03\x12\x11\n\textraData\x18\r \x01(\t\x12\x0c\n\x04size\x18\x0e \x01(\x03\x12\x10\n\x08gasLimit\x18\x0f \x01(\x03\x12\x0f\n\x07gasUsed\x18\x10 \x01(\x03\x12\x15\n\rbaseFeePerGas\x18\x11 \x01(\x03\x12\x11\n\ttimestamp\x18\x12 \x01(\x03\x12\x14\n\x0ctransactions\x18\x13 \x03(\t\x12\x0e\n\x06uncles\x18\x14 \x03(\t\"\xe4\x01\n\x0bTransaction\x12\x11\n\tblockHash\x18\x01 \x01(\t\x12\x13\n\x0b\x62lockNumber\x18\x02 \x01(\x03\x12\x0c\n\x04\x66rom\x18\x03 \x01(\t\x12\x0b\n\x03gas\x18\x04 \x01(\x03\x12\x10\n\x08gasPrice\x18\x05 \x01(\x03\x12\x0c\n\x04hash\x18\x06 \x01(\t\x12\r\n\x05input\x18\x07 \x01(\t\x12\r\n\x05nonce\x18\x08 \x01(\t\x12\n\n\x02to\x18\t \x01(\t\x12\x18\n\x10transactionIndex\x18\n \x01(\x03\x12\r\n\x05value\x18\x0b \x01(\x03\x12\t\n\x01v\x18\x0c \x01(\x03\x12\t\n\x01r\x18\r \x01(\t\x12\t\n\x01s\x18\x0e \x01(\t\"\xb2\x01\n\x03Log\x12\x0f\n\x07removed\x18\x01 \x01(\x08\x12\x10\n\x08logIndex\x18\x02 \x01(\x03\x12\x18\n\x10transactionIndex\x18\x03 \x01(\x03\x12\x17\n\x0ftransactionHash\x18\x04 \x01(\t\x12\x11\n\tblockHash\x18\x05 \x01(\t\x12\x13\n\x0b\x62lockNumber\x18\x06 \x01(\x03\x12\x0f\n\x07\x61\x64\x64ress\x18\x07 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x08 \x01(\t\x12\x0e\n\x06topics\x18\t \x03(\t\"\xb2\x02\n\x07Receipt\x12\x17\n\x0ftransactionHash\x18\x01 \x01(\t\x12\x18\n\x10transactionIndex\x18\x02 \x01(\x03\x12\x11\n\tblockHash\x18\x03 \x01(\t\x12\x13\n\x0b\x62lockNumber\x18\x04 \x01(\x03\x12\x0c\n\x04\x66rom\x18\x05 \x01(\t\x12\n\n\x02to\x18\x06 \x01(\t\x12\x19\n\x11\x63umulativeGasUsed\x18\x07 \x01(\x03\x12\x19\n\x11\x65\x66\x66\x65\x63tiveGasPrice\x18\x08 \x01(\x03\x12\x10\n\x08gas_used\x18\t \x01(\x03\x12\x17\n\x0f\x63ontractAddress\x18\n \x01(\t\x12\x12\n\x04logs\x18\x0b \x03(\x0b\x32\x04.Log\x12\x11\n\tlogsBloom\x18\x0c \x01(\t\x12\x0c\n\x04type\x18\r \x01(\t\x12\x0c\n\x04root\x18\x0e \x01(\t\x12\x0e\n\x06status\x18\x0f \x01(\x08\"\x9f\x01\n\tStructLog\x12\n\n\x02pc\x18\x01 \x01(\x03\x12\n\n\x02op\x18\x02 \x01(\t\x12\x0b\n\x03gas\x18\x03 \x01(\x03\x12\x0f\n\x07gasCost\x18\x04 \x01(\x03\x12\r\n\x05\x64\x65pth\x18\x05 \x01(\x03\x12\r\n\x05\x65rror\x18\x06 \x01(\t\x12\r\n\x05stack\x18\x07 \x03(\t\x12\x0e\n\x06memory\x18\x08 \x03(\t\x12\x0f\n\x07storage\x18\t \x01(\t\x12\x0e\n\x06refund\x18\n \x01(\x03\"Y\n\x05Trace\x12\x0e\n\x06\x66\x61iled\x18\x01 \x01(\x08\x12\x0b\n\x03gas\x18\x02 \x01(\x03\x12\x13\n\x0breturnValue\x18\x03 \x01(\t\x12\x1e\n\nStructLogs\x18\x04 \x03(\x0b\x32\n.StructLogb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'evm_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _BLOCK._serialized_start=14
  _BLOCK._serialized_end=400
  _TRANSACTION._serialized_start=403
  _TRANSACTION._serialized_end=631
  _LOG._serialized_start=634
  _LOG._serialized_end=812
  _RECEIPT._serialized_start=815
  _RECEIPT._serialized_end=1121
  _STRUCTLOG._serialized_start=1124
  _STRUCTLOG._serialized_end=1283
  _TRACE._serialized_start=1285
  _TRACE._serialized_end=1374
# @@protoc_insertion_point(module_scope)