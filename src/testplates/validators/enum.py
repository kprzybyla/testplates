__all__ = ["enum_validator"]

from enum import Enum
from typing import Type, TypeVar, Callable, Optional

from .type import type_validator, validate_any
from .exceptions import MemberValidationError

_T = TypeVar("_T")


def enum_validator(
    enum_type: Type[Enum], validate_value: Callable[[_T], Optional[Exception]] = validate_any, /
) -> Callable[[_T], Optional[Exception]]:
    members = enum_type.__members__.values()

    for member in members:
        error = validate_value(member.value)

        if error is not None:
            raise MemberValidationError(enum_type, member, error)

    validate_enum_type = type_validator(allowed_types=enum_type)

    def validate(data: _T) -> Optional[Exception]:
        return validate_enum_type(data)

    return validate
