__all__ = ["boolean_validator"]

from typing import Any, Final

import testplates

from testplates.result import Result, Success

from .utils import Validator
from .type import type_validator
from .exceptions import ValidationError

boolean_type_validator: Final[Validator] = Success.get_value(type_validator(bool))


class BooleanValidator:

    __slots__ = ()

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{boolean_validator.__name__}()"

    def __call__(self, data: Any) -> Result[None, ValidationError]:
        return boolean_type_validator(data)


# @lru_cache(maxsize=1, typed=True)
def boolean_validator() -> Result[Validator, ValidationError]:
    return Success(BooleanValidator())
