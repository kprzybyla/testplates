__all__ = ["enum_validator"]

from enum import Enum, EnumMeta
from typing import Any, Iterable

import testplates

from testplates.result import Result, Success, Failure

from .utils import Validator
from .type import type_validator
from .passthrough import passthrough_validator
from .exceptions import ValidationError, MemberValidationError


class EnumValidator:

    __slots__ = ("enum_type", "enum_type_validator", "enum_member_validator")

    def __init__(
        self,
        enum_type: EnumMeta,
        enum_type_validator: Validator,
        enum_member_validator: Validator,
    ) -> None:
        self.enum_type = enum_type
        self.enum_type_validator = enum_type_validator
        self.enum_member_validator = enum_member_validator

    def __repr__(self) -> str:
        parameters = f"{self.enum_type}, {self.enum_member_validator}"

        return f"{testplates.__name__}.{enum_validator.__name__}({parameters})"

    def __call__(self, data: Any) -> Result[None, ValidationError]:
        return self.enum_type_validator(data)


# @lru_cache(maxsize=128, typed=True)
def enum_validator(
    enum_type: EnumMeta, enum_member_validator: Validator = passthrough_validator, /
) -> Result[Validator, ValidationError]:
    members: Iterable[Enum] = enum_type.__members__.values()

    for member in members:
        result = enum_member_validator(member.value)

        if result.is_failure:
            return Failure(MemberValidationError(enum_type, member, result.error))

    enum_type_validator = type_validator(enum_type)

    if enum_type_validator.is_failure:
        return Failure.from_result(enum_type_validator)

    return Success(EnumValidator(enum_type, enum_type_validator.value, enum_member_validator))
