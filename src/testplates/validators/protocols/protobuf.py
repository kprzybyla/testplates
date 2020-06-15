__all__ = [
    "bool",
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
    "float",
    "double",
    "string",
    "bytes",
    "enum",
    "repeated",
    "map",
    "message",
    "one_of",
]

from typing import TypeVar, Tuple, Sequence, Mapping, Callable, Optional, Final

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


bool_ = validators.boolean_validator
enum = validators.enum_validator


def int32() -> Callable[[int], Optional[Exception]]:
    validate_int32 = validators.integer_validator(
        minimum_value=INT32_MINIMUM, maximum_value=INT32_MAXIMUM
    )

    def validate(data: int) -> Optional[Exception]:
        return validate_int32(data)

    return validate


def int64() -> Callable[[int], Optional[Exception]]:
    validate_int64 = validators.integer_validator(
        minimum_value=INT64_MINIMUM, maximum_value=INT64_MAXIMUM
    )

    def validate(data: int) -> Optional[Exception]:
        return validate_int64(data)

    return validate


def uint32() -> Callable[[int], Optional[Exception]]:
    validate_uint32 = validators.integer_validator(
        minimum_value=UINT32_MINIMUM, maximum_value=UINT32_MAXIMUM
    )

    def validate(data: int) -> Optional[Exception]:
        return validate_uint32(data)

    return validate


def uint64() -> Callable[[int], Optional[Exception]]:
    validate_uint64 = validators.integer_validator(
        minimum_value=UINT64_MINIMUM, maximum_value=UINT64_MAXIMUM
    )

    def validate(data: int) -> Optional[Exception]:
        return validate_uint64(data)

    return validate


def sint32() -> Callable[[int], Optional[Exception]]:
    validate_sint32 = validators.integer_validator(
        minimum_value=INT32_MINIMUM, maximum_value=INT32_MAXIMUM
    )

    def validate(data: int) -> Optional[Exception]:
        return validate_sint32(data)

    return validate


def sint64() -> Callable[[int], Optional[Exception]]:
    validate_sint64 = validators.integer_validator(
        minimum_value=INT64_MINIMUM, maximum_value=INT64_MAXIMUM
    )

    def validate(data: int) -> Optional[Exception]:
        return validate_sint64(data)

    return validate


def fixed32() -> Callable[[int], Optional[Exception]]:
    validate_fixed32 = validators.integer_validator(
        minimum_value=UINT32_MINIMUM, maximum_value=UINT32_MAXIMUM
    )

    def validate(data: int) -> Optional[Exception]:
        return validate_fixed32(data)

    return validate


def fixed64() -> Callable[[int], Optional[Exception]]:
    validate_fixed64 = validators.integer_validator(
        minimum_value=UINT64_MINIMUM, maximum_value=UINT64_MAXIMUM
    )

    def validate(data: int) -> Optional[Exception]:
        return validate_fixed64(data)

    return validate


def sfixed32() -> Callable[[int], Optional[Exception]]:
    validate_sfixed32 = validators.integer_validator(
        minimum_value=INT32_MINIMUM, maximum_value=INT32_MAXIMUM
    )

    def validate(data: int) -> Optional[Exception]:
        return validate_sfixed32(data)

    return validate


def sfixed64() -> Callable[[int], Optional[Exception]]:
    validate_sfixed64 = validators.integer_validator(
        minimum_value=INT64_MINIMUM, maximum_value=INT64_MAXIMUM
    )

    def validate(data: int) -> Optional[Exception]:
        return validate_sfixed64(data)

    return validate


def float_() -> Callable[[float], Optional[Exception]]:
    validate_float = validators.float_validator(
        minimum_value=..., maximum_value=...  # type: ignore
    )

    def validate(data: float) -> Optional[Exception]:
        return validate_float(data)

    return validate


def double() -> Callable[[float], Optional[Exception]]:
    validate_double = validators.float_validator(
        minimum_value=..., maximum_value=...  # type: ignore
    )

    def validate(data: float) -> Optional[Exception]:
        return validate_double(data)

    return validate


def string() -> Callable[[str], Optional[Exception]]:
    validate_string = validators.string_validator(maximum_length=STRING_MAXIMUM_LENGTH)

    def validate(data: str) -> Optional[Exception]:
        return validate_string(data)

    return validate


def bytes_() -> Callable[[bytes], Optional[Exception]]:
    validate_bytes = validators.bytes_validator(maximum_length=BYTES_MAXIMUM_LENGTH)

    def validate(data: bytes) -> Optional[Exception]:
        return validate_bytes(data)

    return validate


# TODO(kprzybyla): Implement below types validators


def repeated() -> Callable[[Sequence[_T]], Optional[Exception]]:
    def validate(data: Sequence[_T]) -> Optional[Exception]:
        raise NotImplementedError(data)

    return validate


def map_() -> Callable[[Mapping[str, _T]], Optional[Exception]]:
    def validate(data: Mapping[str, _T]) -> Optional[Exception]:
        raise NotImplementedError(data)

    return validate


def message() -> Callable[[Mapping[str, _T]], Optional[Exception]]:
    def validate(data: Mapping[str, _T]) -> Optional[Exception]:
        raise NotImplementedError(data)

    return validate


def one_of() -> Callable[[Tuple[str, _T]], Optional[Exception]]:
    def validate(data: Tuple[str, _T]) -> Optional[Exception]:
        raise NotImplementedError(data)

    return validate


bool = bool_
float = float_
bytes = bytes_
map = map_
