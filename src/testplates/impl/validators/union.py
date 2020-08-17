__all__ = ["UnionValidator"]

from typing import Any, Mapping, Final

from resultful import success, failure, unwrap_failure, Result

import testplates

from testplates.impl.base import TestplatesError

from .utils import Validator
from .type import TypeValidator
from .exceptions import InvalidKeyError, ChoiceValidationError

union_type_validator: Final[Validator] = TypeValidator(tuple)


class UnionValidator:

    __slots__ = ("choices",)

    def __init__(self, choices: Mapping[str, Validator], /) -> None:
        self.choices = choices

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{type(self).__name__}({self.choices})"

    def __call__(self, data: Any, /) -> Result[None, TestplatesError]:
        if not (result := union_type_validator(data)):
            return failure(result)

        key, value = data
        choice_validator = self.choices.get(key, None)

        if choice_validator is None:
            return failure(InvalidKeyError(key, data))

        if not (result := choice_validator(value)):
            return failure(ChoiceValidationError(data, unwrap_failure(result)))

        return success(None)
