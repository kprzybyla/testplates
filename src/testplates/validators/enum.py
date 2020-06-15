__all__ = ["enum_validator"]

from enum import Enum, EnumMeta
from typing import Any, TypeVar, Callable, Optional

from .type import type_validator, validate_any
from .exceptions import MemberValidationError

_T = TypeVar("_T")


def enum_validator(
    enum_type: EnumMeta, validate_value: Callable[[Any], Optional[Exception]] = validate_any, /
) -> Callable[[Enum], Optional[Exception]]:
    members = enum_type.__members__.values()

    for member in members:
        error = validate_value(member.value)

        if error is not None:
            raise MemberValidationError(enum_type, member, error)

    validate_enum_type = type_validator(allowed_types=enum_type)

    def validate(data: Enum) -> Optional[Exception]:
        return validate_enum_type(data)

    return validate
