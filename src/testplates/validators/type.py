__all__ = ["type_validator"]

from typing import Any, Tuple

import testplates

from testplates.result import Result, Success, Failure
from testplates.utils import format_like_tuple

from .utils import Validator
from .exceptions import ValidationError, InvalidTypeValueError, InvalidTypeError


class TypeValidator:

    __slots__ = ("allowed_types",)

    def __init__(self, allowed_types: Tuple[type, ...], /) -> None:
        self.allowed_types = allowed_types

    def __repr__(self) -> str:
        allowed_types = format_like_tuple(self.allowed_types)

        return f"{testplates.__name__}.{type_validator.__name__}({allowed_types})"

    def __call__(self, data: Any) -> Result[None, ValidationError]:
        allowed_types = self.allowed_types

        if not isinstance(data, allowed_types):
            return Failure(InvalidTypeError(data, allowed_types))

        return Success(None)


# @lru_cache(maxsize=128, typed=True)
def type_validator(*allowed_types: type) -> Result[Validator, ValidationError]:
    for allowed_type in allowed_types:
        if (result := validate_type(allowed_type)).is_failure:
            return Failure.from_result(result)

    return Success(TypeValidator(allowed_types))


def validate_type(allowed_type: type) -> Result[None, ValidationError]:
    try:
        isinstance(object, allowed_type)
    except TypeError:
        return Failure(InvalidTypeValueError(allowed_type))
    else:
        return Success(None)
