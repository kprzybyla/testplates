__all__ = ["Mapping"]

import typing

from typing import Type, TypeVar, Generic, Iterable

from .base_validator import BaseValidator
from .exceptions import (
    ValidationError,
    RequiredKeyMissingError,
    RequiredKeyValidatorMissingError,
    FieldValidationError,
)

_T = TypeVar("_T")


class Mapping(BaseValidator[typing.Mapping[str, _T]], Generic[_T]):

    __slots__ = ("_required", "_fields")

    def __init__(self, required: Iterable[str] = (), /, **fields: BaseValidator[_T]) -> None:
        self._required = [name for name in required]
        self._fields = fields

        for key in self._required:
            if key not in self._fields.keys():
                raise RequiredKeyValidatorMissingError(self._required, self._fields)

    @property
    def allowed_types(self) -> Type[typing.Mapping]:
        return typing.Mapping

    def validate(self, data: typing.Mapping[str, _T]) -> None:
        super().validate(data)

        for key in self._required:
            if key not in data.keys():
                raise RequiredKeyMissingError(data, key)

        for key, value in data.items():
            try:
                self._fields[key].validate(value)
            except ValidationError as error:
                raise FieldValidationError(data, key, error) from None
