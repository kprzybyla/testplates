__all__ = ["union_validator"]

from typing import Any, Mapping, Final

import testplates

from testplates.result import Result, Success, Failure

from .utils import Validator
from .type import type_validator
from .exceptions import ValidationError, InvalidKeyError, ChoiceValidationError

union_type_validator: Final[Validator] = Success.get_value(type_validator(tuple))


class UnionValidator:

    __slots__ = ("choices",)

    def __init__(self, choices: Mapping[str, Validator], /) -> None:
        self.choices = choices

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{union_validator.__name__}({self.choices})"

    # noinspection PyTypeChecker
    def __call__(self, data: Any) -> Result[None, ValidationError]:
        if (error := union_type_validator(data)).is_failure:
            return Failure.from_result(error)

        key, value = data

        choice_validator = self.choices.get(key, None)

        if choice_validator is None:
            return Failure(InvalidKeyError(data))

        if (error := choice_validator(value)).is_failure:
            return Failure(ChoiceValidationError(data, error))

        return Success(None)


# @lru_cache(maxsize=128, typed=True)
def union_validator(choices: Mapping[str, Validator], /) -> Result[Validator, ValidationError]:
    return Success(UnionValidator(choices))
