# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: bike.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'bike.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nbike.proto\x1a\x1bgoogle/protobuf/empty.proto\"\xae\x01\n\x07Station\x12\x14\n\x0cstn_grp_name\x18\x01 \x01(\t\x12\x0e\n\x06stn_id\x18\x02 \x01(\t\x12\x0f\n\x07stn_num\x18\x03 \x01(\t\x12\x10\n\x08stn_name\x18\x04 \x01(\t\x12\x12\n\nstn_addr_1\x18\x05 \x01(\t\x12\x12\n\nstn_addr_2\x18\x06 \x01(\t\x12\x0f\n\x07stn_lat\x18\x07 \x01(\x02\x12\x0f\n\x07stn_lng\x18\x08 \x01(\x02\x12\x10\n\x08hold_num\x18\t \x01(\x05\"8\n\x0bStationList\x12\r\n\x05\x63ount\x18\x01 \x01(\x05\x12\x1a\n\x08stations\x18\x02 \x03(\x0b\x32\x08.Station\"J\n\rStationStatus\x12\x0e\n\x06stn_id\x18\x01 \x01(\t\x12\x10\n\x08stn_name\x18\x02 \x01(\t\x12\x17\n\x0fparked_bike_cnt\x18\x03 \x01(\t2\x88\x01\n\x04\x42ike\x12\x38\n\x0eGetStationList\x12\x16.google.protobuf.Empty\x1a\x0c.StationList\"\x00\x12\x46\n\x18GetRealTimeStationStatus\x12\x16.google.protobuf.Empty\x1a\x0e.StationStatus\"\x00\x30\x01\x42\x0fZ\rprotogen/bikeb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'bike_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\rprotogen/bike'
  _globals['_STATION']._serialized_start=44
  _globals['_STATION']._serialized_end=218
  _globals['_STATIONLIST']._serialized_start=220
  _globals['_STATIONLIST']._serialized_end=276
  _globals['_STATIONSTATUS']._serialized_start=278
  _globals['_STATIONSTATUS']._serialized_end=352
  _globals['_BIKE']._serialized_start=355
  _globals['_BIKE']._serialized_end=491
# @@protoc_insertion_point(module_scope)
