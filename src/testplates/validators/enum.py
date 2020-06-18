__all__ = ["enum_validator"]

from enum import Enum, EnumMeta
from typing import Any, TypeVar, Callable

from testplates.result import Result, Success, Failure

from .type import type_validator
from .utils import validate_any, Validator
from .exceptions import MemberValidationError

_T = TypeVar("_T")


def enum_validator(
    enum_type: EnumMeta, validate_value: Callable[[Any], Result[None]] = validate_any, /
) -> Result[Validator[Enum]]:
    members = enum_type.__members__.values()

    for member in members:
        result = validate_value(member.value)

        if result.is_error:
            return Failure(MemberValidationError(enum_type, member, result.error))

    validate_enum_type = type_validator(allowed_types=enum_type)

    if validate_enum_type.is_error:
        return Failure.from_failure(validate_enum_type)

    def validate(data: Enum) -> Result[None]:
        return validate_enum_type.value(data)

    return Success(validate)
