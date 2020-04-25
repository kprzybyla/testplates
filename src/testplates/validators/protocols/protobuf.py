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


def bool_() -> Callable[[bool], Optional[Exception]]:
    validate_bool = validators.boolean_validator()

    def validate(data: bool) -> Optional[Exception]:
        return validate_bool(data)

    return validate


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


def enum(
    validate_member_value: Callable[[_T], Optional[Exception]],
    members: Mapping[str, _T],
    /,
    *,
    allow_aliases: bool = True,
) -> Callable[[_T], Optional[Exception]]:
    validate_enum = validators.enum_validator(
        validate_member_value, members, allow_aliases=allow_aliases
    )

    def validate(data: _T) -> Optional[Exception]:
        return validate_enum(data)

    return validate


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
