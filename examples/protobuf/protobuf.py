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

from enum import EnumMeta
from typing import Mapping, Final

from testplates import validators, UNLIMITED
from testplates.result import Result
from testplates.impl.base import StructureMeta
from testplates.validators.utils import Validator
from testplates.validators.exceptions import ValidationError

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


def bool_() -> Result[Validator, ValidationError]:
    return bool_validator


def int32() -> Result[Validator, ValidationError]:
    return int32_validator


def int64() -> Result[Validator, ValidationError]:
    return int64_validator


def uint32() -> Result[Validator, ValidationError]:
    return uint32_validator


def uint64() -> Result[Validator, ValidationError]:
    return uint64_validator


def sint32() -> Result[Validator, ValidationError]:
    return sint32_validator


def sint64() -> Result[Validator, ValidationError]:
    return sint64_validator


def fixed32() -> Result[Validator, ValidationError]:
    return fixed32_validator


def fixed64() -> Result[Validator, ValidationError]:
    return fixed64_validator


def sfixed32() -> Result[Validator, ValidationError]:
    return sfixed32_validator


def sfixed64() -> Result[Validator, ValidationError]:
    return sfixed64_validator


def float_() -> Result[Validator, ValidationError]:
    return float_validator


def double() -> Result[Validator, ValidationError]:
    return double_validator


def string() -> Result[Validator, ValidationError]:
    return string_validator


def bytes_() -> Result[Validator, ValidationError]:
    return bytes_validator


def enum(
    enum_type: EnumMeta, enum_member_validator: Validator, /
) -> Result[Validator, ValidationError]:
    return validators.enum_validator(enum_type, enum_member_validator)


def repeated(item_validator: Validator, /) -> Result[Validator, ValidationError]:
    return validators.sequence_validator(
        item_validator, minimum_size=UNLIMITED, maximum_size=UNLIMITED
    )


def map_(structure_type: StructureMeta) -> Result[Validator, ValidationError]:
    return validators.mapping_validator(structure_type)


def message(structure_type: StructureMeta) -> Result[Validator, ValidationError]:
    return validators.mapping_validator(structure_type)


def oneof(choices: Mapping[str, Validator], /) -> Result[Validator, ValidationError]:
    return validators.union_validator(choices)
