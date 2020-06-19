__all__ = [
    "bool_",
    "int32",
    "int64",
    "uint32",
    "uint64",
    "sint32",
    "sint64",
    "fixed32",
    "fixed64",
    "sfixed32",
    "sfixed64",
    "float_",
    "double",
    "string",
    "bytes_",
    "enum",
    "repeated",
    "map_",
    "message",
    "oneof",
]

from enum import Enum, EnumMeta
from typing import TypeVar, Tuple, Sequence, Mapping, Final

from testplates import validators
from testplates.result import Result, Failure
from testplates.validators.utils import Validator

_T = TypeVar("_T")

INT32_MINIMUM: Final[int] = -(2 ** 31)
INT32_MAXIMUM: Final[int] = (2 ** 31) - 1

INT64_MINIMUM: Final[int] = -(2 ** 63)
INT64_MAXIMUM: Final[int] = (2 ** 63) - 1

UINT32_MINIMUM: Final[int] = 0
UINT32_MAXIMUM: Final[int] = (2 ** 32) - 1

UINT64_MINIMUM: Final[int] = 0
UINT64_MAXIMUM: Final[int] = (2 ** 64) - 1

FLOAT_MINIMUM: Final[float] = 0.0
FLOAT_MAXIMUM: Final[float] = 0.0

DOUBLE_MINIMUM: Final[float] = 0.0
DOUBLE_MAXIMUM: Final[float] = 0.0

STRING_MAXIMUM_LENGTH: Final[int] = 2 ** 32
BYTES_MAXIMUM_LENGTH: Final[int] = 2 ** 32

bool_validator = validators.boolean_validator()

int32_validator = validators.integer_validator(
    minimum_value=INT32_MINIMUM, maximum_value=INT32_MAXIMUM
)

int64_validator = validators.integer_validator(
    minimum_value=INT64_MINIMUM, maximum_value=INT64_MAXIMUM
)

uint32_validator = validators.integer_validator(
    minimum_value=UINT32_MINIMUM, maximum_value=UINT32_MAXIMUM
)

uint64_validator = validators.integer_validator(
    minimum_value=UINT64_MINIMUM, maximum_value=UINT64_MAXIMUM
)

sint32_validator = validators.integer_validator(
    minimum_value=INT32_MINIMUM, maximum_value=INT32_MAXIMUM
)

sint64_validator = validators.integer_validator(
    minimum_value=INT64_MINIMUM, maximum_value=INT64_MAXIMUM
)

fixed32_validator = validators.integer_validator(
    minimum_value=UINT32_MINIMUM, maximum_value=UINT32_MAXIMUM
)

fixed64_validator = validators.integer_validator(
    minimum_value=UINT64_MINIMUM, maximum_value=UINT64_MAXIMUM
)

sfixed32_validator = validators.integer_validator(
    minimum_value=INT32_MINIMUM, maximum_value=INT32_MAXIMUM
)

sfixed64_validator = validators.integer_validator(
    minimum_value=INT64_MINIMUM, maximum_value=INT64_MAXIMUM
)

float_validator = validators.float_validator(
    minimum_value=FLOAT_MINIMUM, maximum_value=FLOAT_MAXIMUM
)

double_validator = validators.float_validator(
    minimum_value=DOUBLE_MINIMUM, maximum_value=DOUBLE_MAXIMUM
)

string_validator = validators.string_validator(maximum_length=STRING_MAXIMUM_LENGTH)
bytes_validator = validators.bytes_validator(maximum_length=BYTES_MAXIMUM_LENGTH)


def bool_() -> Result[Validator[bool]]:
    return bool_validator


def int32() -> Result[Validator[int]]:
    return int32_validator


def int64() -> Result[Validator[int]]:
    return int64_validator


def uint32() -> Result[Validator[int]]:
    return uint32_validator


def uint64() -> Result[Validator[int]]:
    return uint64_validator


def sint32() -> Result[Validator[int]]:
    return sint32_validator


def sint64() -> Result[Validator[int]]:
    return sint64_validator


def fixed32() -> Result[Validator[int]]:
    return fixed32_validator


def fixed64() -> Result[Validator[int]]:
    return fixed64_validator


def sfixed32() -> Result[Validator[int]]:
    return sfixed32_validator


def sfixed64() -> Result[Validator[int]]:
    return sfixed64_validator


def float_() -> Result[Validator[float]]:
    return float_validator


def double() -> Result[Validator[float]]:
    return double_validator


def string() -> Result[Validator[str]]:
    return string_validator


def bytes_() -> Result[Validator[bytes]]:
    return bytes_validator


def enum(enum_type: EnumMeta, validator: Validator, /) -> Result[Validator[Enum]]:
    return validators.enum_validator(enum_type, validator)


# TODO(kprzybyla): Implement below types validators


def repeated() -> Result[Validator[Sequence[_T]]]:
    return Failure(NotImplementedError())


def map_() -> Result[Validator[Mapping[str, _T]]]:
    return Failure(NotImplementedError())


def message() -> Result[Validator[Mapping[str, _T]]]:
    return Failure(NotImplementedError())


def oneof() -> Result[Validator[Tuple[str, _T]]]:
    return Failure(NotImplementedError())
