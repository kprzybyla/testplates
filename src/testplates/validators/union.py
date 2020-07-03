__all__ = ["union_validator"]

from typing import TypeVar, Tuple, Mapping, Final

import testplates

from testplates.result import Result, Success, Failure
from testplates.utils import format_like_dict

from .type import type_validator
from .utils import Validator
from .exceptions import InvalidKeyError, ChoiceValidationError

_T = TypeVar("_T")

union_type_validator: Final[Validator[tuple]] = type_validator(tuple).value


class UnionValidator:

    __slots__ = ("choices",)

    def __init__(self, choices: Mapping[str, Validator[_T]], /) -> None:
        self.choices = choices

    def __repr__(self) -> str:
        choices = format_like_dict(self.choices)

        return f"{testplates.__name__}.{union_validator.__name__}({choices})"

    def __call__(self, data: Tuple[str, _T]) -> Result[None]:
        if (error := union_type_validator(data)) is not None:
            return Failure.from_failure(error)

        key, value = data

        choice_validator = self.choices.get(key, None)

        if choice_validator is None:
            return Failure(InvalidKeyError(data, key))

        if (error := choice_validator(value)) is not None:
            return Failure(ChoiceValidationError(data, key, error))

        return Success(None)


# @lru_cache(maxsize=128, typed=True)
def union_validator(choices: Mapping[str, Validator[_T]], /) -> Result[Validator[Tuple[str, _T]]]:
    return Success(UnionValidator(choices))
