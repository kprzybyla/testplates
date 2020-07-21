__all__ = [
    "passthrough_validator",
    "type_validator",
    "boolean_validator",
    "integer_validator",
    "any_string_validator",
    "string_validator",
    "bytes_validator",
    "enum_validator",
    "sequence_validator",
    "mapping_validator",
    "union_validator",
    "Validator",
]

import re

from enum import Enum, EnumMeta
from typing import (
    overload,
    Any,
    AnyStr,
    Iterable,
    Mapping,
    Optional,
    Pattern as Regex,
    Callable,
    Final,
)

from testplates.impl.base import get_value_boundaries, get_length_boundaries, StructureMeta
from testplates.impl.validators import (
    TypeValidator,
    PassthroughValidator,
    BooleanValidator,
    IntegerValidator,
    AnyStringValidator,
    StringValidator,
    BytesValidator,
    EnumValidator,
    SequenceValidator,
    MappingValidator,
    UnionValidator,
)

from .value import Boundary
from .result import success, failure, unwrap_success, unwrap_failure, Result
from .exceptions import ValidationError, InvalidTypeValueError, MemberValidationError

Validator: Final = Callable[[Any], Result[None, ValidationError]]

passthrough_validator = PassthroughValidator()


# noinspection PyTypeChecker
# @lru_cache(maxsize=128, typed=True)
def type_validator(*allowed_types: type) -> Result[Validator, ValidationError]:
    for allowed_type in allowed_types:
        if (result := validate_type(allowed_type)).is_failure:
            return failure(result)

    return success(TypeValidator(allowed_types))


# noinspection PyTypeChecker
def validate_type(allowed_type: type) -> Result[None, ValidationError]:
    try:
        isinstance(object, allowed_type)
    except TypeError:
        return failure(InvalidTypeValueError(allowed_type))
    else:
        return success(None)


# @lru_cache(maxsize=1, typed=True)
def boolean_validator() -> Result[Validator, ValidationError]:
    return success(BooleanValidator())


@overload
def integer_validator(
    *,
    minimum: Optional[Boundary[int]] = None,
    maximum: Optional[Boundary[int]] = None,
    allow_boolean: bool = False,
) -> Result[Validator, ValidationError]:
    ...


@overload
def integer_validator(
    *,
    minimum: Optional[Boundary[int]] = None,
    exclusive_maximum: Optional[Boundary[int]] = None,
    allow_boolean: bool = False,
) -> Result[Validator, ValidationError]:
    ...


@overload
def integer_validator(
    *,
    exclusive_minimum: Optional[Boundary[int]] = None,
    maximum: Optional[Boundary[int]] = None,
    allow_boolean: bool = False,
) -> Result[Validator, ValidationError]:
    ...


@overload
def integer_validator(
    *,
    exclusive_minimum: Optional[Boundary[int]] = None,
    exclusive_maximum: Optional[Boundary[int]] = None,
    allow_boolean: bool = False,
) -> Result[Validator, ValidationError]:
    ...


# noinspection PyTypeChecker
def integer_validator(
    *,
    minimum: Optional[Boundary[int]] = None,
    maximum: Optional[Boundary[int]] = None,
    exclusive_minimum: Optional[Boundary[int]] = None,
    exclusive_maximum: Optional[Boundary[int]] = None,
    allow_boolean: bool = False,
) -> Result[Validator, ValidationError]:
    result = get_value_boundaries(
        inclusive_minimum=minimum,
        inclusive_maximum=maximum,
        exclusive_minimum=exclusive_minimum,
        exclusive_maximum=exclusive_maximum,
    )

    if result.is_failure:
        return failure(result)

    minimum, maximum = unwrap_success(result)

    return success(IntegerValidator(minimum, maximum, allow_boolean))


@overload
def any_string_validator(
    *, length: Optional[int] = None, pattern: Optional[AnyStr] = None
) -> Result[Validator, ValidationError]:
    ...


@overload
def any_string_validator(
    *,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[AnyStr] = None,
) -> Result[Validator, ValidationError]:
    ...


# noinspection PyTypeChecker
def any_string_validator(
    *,
    length: Optional[int] = None,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[AnyStr] = None,
) -> Result[Validator, ValidationError]:
    result = get_length_boundaries(
        inclusive_minimum=minimum_length, inclusive_maximum=maximum_length
    )

    if result.is_failure:
        return failure(result)

    minimum, maximum = unwrap_success(result)
    regex = get_regex(pattern)

    return success(AnyStringValidator(length, minimum, maximum, regex))


@overload
def string_validator(
    *, length: Optional[int] = None, pattern: Optional[str] = None
) -> Result[Validator, ValidationError]:
    ...


@overload
def string_validator(
    *,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[str] = None,
) -> Result[Validator, ValidationError]:
    ...


# noinspection PyTypeChecker
def string_validator(
    *,
    length: Optional[int] = None,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[str] = None,
) -> Result[Validator, ValidationError]:
    result = get_length_boundaries(
        inclusive_minimum=minimum_length, inclusive_maximum=maximum_length
    )

    if result.is_failure:
        return failure(result)

    minimum, maximum = unwrap_success(result)
    regex = get_regex(pattern)

    return success(StringValidator(length, minimum, maximum, regex))


@overload
def bytes_validator(
    *, length: Optional[int] = None, pattern: Optional[bytes] = None
) -> Result[Validator, ValidationError]:
    ...


@overload
def bytes_validator(
    *,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[bytes] = None,
) -> Result[Validator, ValidationError]:
    ...


# noinspection PyTypeChecker
def bytes_validator(
    *,
    length: Optional[int] = None,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[bytes] = None,
) -> Result[Validator, ValidationError]:
    result = get_length_boundaries(
        inclusive_minimum=minimum_length, inclusive_maximum=maximum_length
    )

    if result.is_failure:
        return failure(result)

    minimum, maximum = unwrap_success(result)
    regex = get_regex(pattern)

    return success(BytesValidator(length, minimum, maximum, regex))


def get_regex(pattern: Optional[AnyStr]) -> Optional[Regex[AnyStr]]:
    return re.compile(pattern) if pattern is not None else None


# noinspection PyTypeChecker
# @lru_cache(maxsize=128, typed=True)
def enum_validator(
    enum_type: EnumMeta, enum_member_validator: Validator = passthrough_validator, /
) -> Result[Validator, ValidationError]:
    members: Iterable[Enum] = enum_type.__members__.values()

    for member in members:
        result = enum_member_validator(member.value)

        if result.is_failure:
            return failure(MemberValidationError(enum_type, member, unwrap_failure(result)))

    enum_type_validator_result = type_validator(enum_type)

    if enum_type_validator_result.is_failure:
        return failure(enum_type_validator_result)

    enum_type_validator = unwrap_success(enum_type_validator_result)

    return success(EnumValidator(enum_type, enum_type_validator, enum_member_validator))


# noinspection PyTypeChecker
def sequence_validator(
    item_validator: Validator = passthrough_validator,
    /,
    *,
    minimum_size: Optional[Boundary[int]] = None,
    maximum_size: Optional[Boundary[int]] = None,
    unique_items: bool = False,
) -> Result[Validator, ValidationError]:
    result = get_length_boundaries(inclusive_minimum=minimum_size, inclusive_maximum=maximum_size)

    if result.is_failure:
        return failure(result)

    minimum, maximum = unwrap_success(result)

    return success(SequenceValidator(item_validator, minimum, maximum, unique_items))


# @lru_cache(maxsize=128, typed=True)
def mapping_validator(structure_type: StructureMeta) -> Result[Validator, ValidationError]:
    return success(MappingValidator(structure_type))


# @lru_cache(maxsize=128, typed=True)
def union_validator(choices: Mapping[str, Validator], /) -> Result[Validator, ValidationError]:
    return success(UnionValidator(choices))
