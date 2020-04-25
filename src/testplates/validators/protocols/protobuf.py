__all__ = [
    "Bool",
    "Int32",
    "Int64",
    "UInt32",
    "UInt64",
    "SInt32",
    "SInt64",
    "Fixed32",
    "Fixed64",
    "SFixed32",
    "SFixed64",
    "Float",
    "Double",
    "String",
    "Bytes",
    "Enum",
    "Repeated",
    "Map",
    "Message",
    "OneOf",
]

from typing import TypeVar, Final

from testplates import validators

_T = TypeVar("_T")

INT32_MINIMUM: Final[int] = -(2 ** 31)
INT32_MAXIMUM: Final[int] = (2 ** 31) - 1

INT64_MINIMUM: Final[int] = -(2 ** 63)
INT64_MAXIMUM: Final[int] = (2 ** 63) - 1

UINT32_MINIMUM: Final[int] = 0
UINT32_MAXIMUM: Final[int] = (2 ** 32) - 1

UINT64_MINIMUM: Final[int] = 0
UINT64_MAXIMUM: Final[int] = (2 ** 64) - 1

STRING_MAXIMUM_LENGTH: Final[int] = 2 ** 32
BYTES_MAXIMUM_LENGTH: Final[int] = 2 ** 32


class Bool(validators.Boolean):

    __slots__ = ()


class Int32(validators.Integer):

    __slots__ = ()

    def __init__(self) -> None:
        super().__init__(minimum=INT32_MINIMUM, maximum=INT32_MAXIMUM)


class Int64(validators.Integer):

    __slots__ = ()

    def __init__(self) -> None:
        super().__init__(minimum=INT64_MINIMUM, maximum=INT64_MAXIMUM)


class UInt32(validators.Integer):

    __slots__ = ()

    def __init__(self) -> None:
        super().__init__(minimum=UINT32_MINIMUM, maximum=UINT32_MAXIMUM)


class UInt64(validators.Integer):

    __slots__ = ()

    def __init__(self) -> None:
        super().__init__(minimum=UINT64_MINIMUM, maximum=UINT64_MAXIMUM)


class SInt32(validators.Integer):

    __slots__ = ()

    def __init__(self) -> None:
        super().__init__(minimum=INT32_MINIMUM, maximum=INT32_MAXIMUM)


class SInt64(validators.Integer):

    __slots__ = ()

    def __init__(self) -> None:
        super().__init__(minimum=INT64_MINIMUM, maximum=INT64_MAXIMUM)


class Fixed32(validators.Integer):

    __slots__ = ()

    def __init__(self) -> None:
        super().__init__(minimum=UINT32_MINIMUM, maximum=UINT32_MAXIMUM)


class Fixed64(validators.Integer):

    __slots__ = ()

    def __init__(self) -> None:
        super().__init__(minimum=UINT64_MINIMUM, maximum=UINT64_MAXIMUM)


class SFixed32(validators.Integer):

    __slots__ = ()

    def __init__(self) -> None:
        super().__init__(minimum=INT32_MINIMUM, maximum=INT32_MAXIMUM)


class SFixed64(validators.Integer):

    __slots__ = ()

    def __init__(self) -> None:
        super().__init__(minimum=INT64_MINIMUM, maximum=INT64_MAXIMUM)


class Float(validators.Float):

    __slots__ = ()

    def __init__(self) -> None:
        super().__init__(minimum=..., maximum=...)


class Double(validators.Float):

    __slots__ = ()

    def __init__(self) -> None:
        super().__init__(minimum=..., maximum=...)


class String(validators.String):

    __slots__ = ()

    def __init__(self) -> None:
        super().__init__(maximum_length=STRING_MAXIMUM_LENGTH)


class Bytes(validators.Bytes):

    __slots__ = ()

    def __init__(self) -> None:
        super().__init__(maximum_length=BYTES_MAXIMUM_LENGTH)


class Enum(validators.Enum[_T]):

    __slots__ = ()


class Repeated(validators.Sequence[_T]):
    pass


class Map(validators.Mapping[_T]):
    pass


class Message(validators.Mapping[_T]):
    pass


class OneOf(validators.Union[_T]):
    pass
