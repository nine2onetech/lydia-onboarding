from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Greetings(_message.Message):
    __slots__ = ("name", "body")
    NAME_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    name: str
    body: str
    def __init__(self, name: _Optional[str] = ..., body: _Optional[str] = ...) -> None: ...

class BackAtYou(_message.Message):
    __slots__ = ("response",)
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: str
    def __init__(self, response: _Optional[str] = ...) -> None: ...
