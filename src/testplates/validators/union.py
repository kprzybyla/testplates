__all__ = ["Union"]

from typing import Type, TypeVar, Tuple, Mapping

from .base_validator import BaseValidator
from .exceptions import ValidationError, InvalidKeyError, ChoiceValidationError

_T = TypeVar("_T")


class Union(BaseValidator[Tuple[str, _T]]):

    __slots__ = ("_choices",)

    def __init__(self, choices: Mapping[str, BaseValidator[_T]], /):
        self._choices = choices

    @property
    def allowed_types(self) -> Type[Tuple]:
        return tuple

    def validate(self, data: Tuple[str, _T]) -> None:
        super().validate(data)

        key, value = data

        validator = self._choices.get(key, None)

        if validator is None:
            raise InvalidKeyError(data, key)

        try:
            validator.validate(value)
        except ValidationError as error:
            raise ChoiceValidationError(data, key, error) from None
