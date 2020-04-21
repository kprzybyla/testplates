__all__ = ["Enum"]

from typing import TypeVar, Generic

from .base_validator import BaseValidator
from .exceptions import ValidationError, MemberValidationError, ProhibitedValueError

_T = TypeVar("_T")


class Enum(BaseValidator[_T], Generic[_T]):

    __slots__ = ("_validator", "_members")

    def __init__(self, validator: BaseValidator[_T], /, **members: _T) -> None:
        for value in members.values():
            validator.validate(value)

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
