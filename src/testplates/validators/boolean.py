__all__ = ["boolean_validator"]

from typing import Final

import testplates

from testplates.result import Result, Success

from .type import type_validator
from .utils import Validator

boolean_type_validator: Final[Validator[bool]] = type_validator(bool).value


class BooleanValidator:

    __slots__ = ()

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{boolean_validator.__name__}()"

    def __call__(self, data: bool) -> Result[None]:
        return boolean_type_validator(data)


# @lru_cache(maxsize=1, typed=True)
def boolean_validator() -> Result[Validator[bool]]:
    return Success(BooleanValidator())
