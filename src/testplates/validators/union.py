__all__ = ["union_validator"]

from typing import TypeVar, Tuple, Mapping, Callable, Optional

from .type import type_validator
from .exceptions import InvalidKeyError, ChoiceValidationError

_T = TypeVar("_T")

validate_union_type = type_validator(allowed_types=tuple)


def union_validator(
    choices: Mapping[str, Callable[[_T], Optional[Exception]]], /
) -> Callable[[Tuple[str, _T]], Optional[Exception]]:
    def validate(data: Tuple[str, _T]) -> Optional[Exception]:
        if (error := validate_union_type(data)) is not None:
            return error

        key, value = data

        validate_choice = choices.get(key, None)

        if validate_choice is None:
            return InvalidKeyError(data, key)

        if (error := validate_choice(value)) is not None:
            return ChoiceValidationError(data, key, error)

    return validate
