__all__ = ["Enum"]

from typing import TypeVar, Generic, Mapping

from .utils import has_unique_items
from .base_validator import BaseValidator
from .exceptions import (
    ValidationError,
    MemberValidationError,
    ProhibitedValueError,
    EnumAliasesNotAllowed,
)

_T = TypeVar("_T")


class Enum(BaseValidator[_T], Generic[_T]):

    __slots__ = ("_validator", "_members")

    def __init__(
        self,
        validator: BaseValidator[_T],
        members: Mapping[str, _T],
        /,
        *,
        allow_aliases: bool = True,
    ) -> None:
        for value in members.values():
            validator.validate(value)

        if not allow_aliases and not has_unique_items(members.values()):
            raise EnumAliasesNotAllowed()

        self._validator = validator
        self._members = members

    def validate(self, data: _T) -> None:
        try:
            self._validator.validate(data)
        except ValidationError as error:
            raise MemberValidationError(error) from error

        values = self._members.values()

        if data not in values:
            raise ProhibitedValueError(data, values)
