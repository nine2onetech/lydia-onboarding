from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Station(_message.Message):
    __slots__ = ("stn_grp_name", "stn_id", "stn_num", "stn_name", "stn_addr_1", "stn_addr_2", "stn_lat", "stn_lng", "hold_num")
    STN_GRP_NAME_FIELD_NUMBER: _ClassVar[int]
    STN_ID_FIELD_NUMBER: _ClassVar[int]
    STN_NUM_FIELD_NUMBER: _ClassVar[int]
    STN_NAME_FIELD_NUMBER: _ClassVar[int]
    STN_ADDR_1_FIELD_NUMBER: _ClassVar[int]
    STN_ADDR_2_FIELD_NUMBER: _ClassVar[int]
    STN_LAT_FIELD_NUMBER: _ClassVar[int]
    STN_LNG_FIELD_NUMBER: _ClassVar[int]
    HOLD_NUM_FIELD_NUMBER: _ClassVar[int]
    stn_grp_name: str
    stn_id: str
    stn_num: str
    stn_name: str
    stn_addr_1: str
    stn_addr_2: str
    stn_lat: float
    stn_lng: float
    hold_num: int
    def __init__(self, stn_grp_name: _Optional[str] = ..., stn_id: _Optional[str] = ..., stn_num: _Optional[str] = ..., stn_name: _Optional[str] = ..., stn_addr_1: _Optional[str] = ..., stn_addr_2: _Optional[str] = ..., stn_lat: _Optional[float] = ..., stn_lng: _Optional[float] = ..., hold_num: _Optional[int] = ...) -> None: ...

class StationList(_message.Message):
    __slots__ = ("count", "stations")
    COUNT_FIELD_NUMBER: _ClassVar[int]
    STATIONS_FIELD_NUMBER: _ClassVar[int]
    count: int
    stations: _containers.RepeatedCompositeFieldContainer[Station]
    def __init__(self, count: _Optional[int] = ..., stations: _Optional[_Iterable[_Union[Station, _Mapping]]] = ...) -> None: ...

class StationStatus(_message.Message):
    __slots__ = ("stn_id", "stn_name", "parked_bike_cnt")
    STN_ID_FIELD_NUMBER: _ClassVar[int]
    STN_NAME_FIELD_NUMBER: _ClassVar[int]
    PARKED_BIKE_CNT_FIELD_NUMBER: _ClassVar[int]
    stn_id: str
    stn_name: str
    parked_bike_cnt: str
    def __init__(self, stn_id: _Optional[str] = ..., stn_name: _Optional[str] = ..., parked_bike_cnt: _Optional[str] = ...) -> None: ...
