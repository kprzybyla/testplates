__all__ = ["UnionValidator"]

from typing import Any, Mapping, Final

import testplates

from testplates.impl.base import Result, Success, Failure
from testplates.impl.base import TestplatesError

from .utils import Validator
from .type import TypeValidator
from .exceptions import InvalidKeyError, ChoiceValidationError

union_type_validator: Final[Validator] = TypeValidator((tuple,))


class UnionValidator:

    __slots__ = ("choices",)

    def __init__(self, choices: Mapping[str, Validator], /) -> None:
        self.choices = choices

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{type(self).__name__}({self.choices})"

    # noinspection PyTypeChecker
    def __call__(self, data: Any) -> Result[None, TestplatesError]:
        if (error := union_type_validator(data)).is_failure:
            return Failure.from_result(error)

        key, value = data

        choice_validator = self.choices.get(key, None)

        if choice_validator is None:
            return Failure(InvalidKeyError(key, data))

        if (error := choice_validator(value)).is_failure:
            return Failure(ChoiceValidationError(data, error))

        return Success(None)
