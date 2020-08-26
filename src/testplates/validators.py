__all__ = (
    "passthrough_validator",
    "type_validator",
    "boolean_validator",
    "integer_validator",
    "string_validator",
    "bytes_validator",
    "enum_validator",
    "sequence_validator",
    "mapping_validator",
    "union_validator",
)

from enum import (
    Enum,
    EnumMeta,
)

from typing import (
    overload,
    Iterable,
    Mapping,
    Optional,
    Final,
)

from resultful import (
    success,
    failure,
    unwrap_success,
    unwrap_failure,
    Result,
)

from testplates.impl.base import (
    get_pattern,
    get_value_boundaries,
    get_length_boundaries,
    StructureMeta,
)

from testplates.impl.validators import (
    is_classinfo,
    TypeValidator,
    PassthroughValidator,
    BooleanValidator,
    IntegerValidator,
    StringValidator,
    BytesValidator,
    EnumValidator,
    SequenceValidator,
    MappingValidator,
    UnionValidator,
)

from .value import (
    Boundary,
    Validator,
)

from .exceptions import (
    TestplatesError,
    InvalidTypeValueError,
    MemberValidationError,
)

passthrough_validator: Final[PassthroughValidator] = PassthroughValidator()


def type_validator(*allowed_types: type) -> Result[Validator, TestplatesError]:

    """
    ...

    :param allowed_types: ...
    """

    for allowed_type in allowed_types:
        if not is_classinfo(allowed_type):
            return failure(InvalidTypeValueError(allowed_type))

    return success(TypeValidator(*allowed_types))


def boolean_validator() -> Result[Validator, TestplatesError]:

    """
    ...
    """

    return success(BooleanValidator())


@overload
def integer_validator(
    *,
    minimum: Optional[Boundary[int]] = None,
    maximum: Optional[Boundary[int]] = None,
    allow_bool: bool = False,
) -> Result[Validator, TestplatesError]:
    ...


@overload
def integer_validator(
    *,
    minimum: Optional[Boundary[int]] = None,
    exclusive_maximum: Optional[Boundary[int]] = None,
    allow_bool: bool = False,
) -> Result[Validator, TestplatesError]:
    ...


@overload
def integer_validator(
    *,
    exclusive_minimum: Optional[Boundary[int]] = None,
    maximum: Optional[Boundary[int]] = None,
    allow_bool: bool = False,
) -> Result[Validator, TestplatesError]:
    ...


@overload
def integer_validator(
    *,
    exclusive_minimum: Optional[Boundary[int]] = None,
    exclusive_maximum: Optional[Boundary[int]] = None,
    allow_bool: bool = False,
) -> Result[Validator, TestplatesError]:
    ...


def integer_validator(
    *,
    minimum: Optional[Boundary[int]] = None,
    maximum: Optional[Boundary[int]] = None,
    exclusive_minimum: Optional[Boundary[int]] = None,
    exclusive_maximum: Optional[Boundary[int]] = None,
    allow_bool: bool = False,
) -> Result[Validator, TestplatesError]:

    """
    ...

    :param minimum: ...
    :param maximum: ...
    :param exclusive_minimum: ...
    :param exclusive_maximum: ...
    :param allow_bool: ...
    """

    result = get_value_boundaries(
        inclusive_minimum=minimum,
        inclusive_maximum=maximum,
        exclusive_minimum=exclusive_minimum,
        exclusive_maximum=exclusive_maximum,
    )

    if not result:
        return failure(result)

    minimum_value, maximum_value = unwrap_success(result)

    return success(
        IntegerValidator(
            minimum_value=minimum_value,
            maximum_value=maximum_value,
            allow_bool=allow_bool,
        )
    )


def string_validator(
    *,
    minimum_size: Optional[Boundary[int]] = None,
    maximum_size: Optional[Boundary[int]] = None,
    pattern: Optional[str] = None,
) -> Result[Validator, TestplatesError]:

    """
    ...

    :param minimum_size: ...
    :param maximum_size: ...
    :param pattern: ...
    """

    result = get_length_boundaries(inclusive_minimum=minimum_size, inclusive_maximum=maximum_size)

    if not result:
        return failure(result)

    minimum_length, maximum_length = unwrap_success(result)

    return success(
        StringValidator(
            minimum_length=minimum_length,
            maximum_length=maximum_length,
            pattern=get_pattern(pattern),
        )
    )


def bytes_validator(
    *,
    minimum_size: Optional[Boundary[int]] = None,
    maximum_size: Optional[Boundary[int]] = None,
    pattern: Optional[bytes] = None,
) -> Result[Validator, TestplatesError]:

    """
    ...

    :param minimum_size: ...
    :param maximum_size: ...
    :param pattern: ...
    """

    result = get_length_boundaries(inclusive_minimum=minimum_size, inclusive_maximum=maximum_size)

    if not result:
        return failure(result)

    minimum_length, maximum_length = unwrap_success(result)

    return success(
        BytesValidator(
            minimum_length=minimum_length,
            maximum_length=maximum_length,
            pattern=get_pattern(pattern),
        )
    )


def enum_validator(
    enum_type: EnumMeta,
    enum_member_validator: Validator = passthrough_validator,
    /,
) -> Result[Validator, TestplatesError]:

    """
    ...

    :param enum_type: ...
    :param enum_member_validator: ...
    """

    members: Iterable[Enum] = enum_type.__members__.values()

    for member in members:
        result = enum_member_validator(member.value)

        if not result:
            return failure(MemberValidationError(enum_type, member, unwrap_failure(result)))

    enum_type_validator_result = type_validator(enum_type)

    if not enum_type_validator_result:
        return failure(enum_type_validator_result)

    enum_type_validator = unwrap_success(enum_type_validator_result)

    return success(
        EnumValidator(
            enum_type,
            enum_type_validator=enum_type_validator,
            enum_member_validator=enum_member_validator,
        )
    )


def sequence_validator(
    item_validator: Validator = passthrough_validator,
    /,
    *,
    minimum_size: Optional[Boundary[int]] = None,
    maximum_size: Optional[Boundary[int]] = None,
    unique_items: bool = False,
) -> Result[Validator, TestplatesError]:

    """
    ...

    :param item_validator: ...
    :param minimum_size: ...
    :param maximum_size: ...
    :param unique_items: ...
    """

    result = get_length_boundaries(inclusive_minimum=minimum_size, inclusive_maximum=maximum_size)

    if not result:
        return failure(result)

    minimum_length, maximum_length = unwrap_success(result)

    return success(
        SequenceValidator(
            item_validator,
            minimum_length=minimum_length,
            maximum_length=maximum_length,
            unique_items=unique_items,
        )
    )


def mapping_validator(structure_type: StructureMeta, /) -> Result[Validator, TestplatesError]:

    """
    ...

    :param structure_type: ...
    """

    return success(MappingValidator(structure_type))


def union_validator(choices: Mapping[str, Validator], /) -> Result[Validator, TestplatesError]:

    """
    ...

    :param choices: ...
    """

    return success(UnionValidator(choices))
