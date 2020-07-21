__all__ = ["BooleanValidator"]

from typing import Any, Final

import testplates

from testplates.impl.base import Result

from .utils import Validator
from .type import TypeValidator
from .exceptions import ValidationError

boolean_type_validator: Final[Validator] = TypeValidator((bool,))


class BooleanValidator:

    __slots__ = ()

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{type(self).__name__}()"

    def __call__(self, data: Any) -> Result[None, ValidationError]:
        return boolean_type_validator(data)
