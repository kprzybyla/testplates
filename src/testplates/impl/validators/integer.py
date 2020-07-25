__all__ = ["IntegerValidator"]

from typing import Any, Union, Final

from testplates.impl.base import Result, Success, Failure
from testplates.impl.base import fits_minimum, fits_maximum, Limit, UnlimitedType
from testplates.impl.base import TestplatesError

from .type import TypeValidator
from .exceptions import (
    InvalidMinimumValueError,
    InvalidMaximumValueError,
    ProhibitedBoolValueError,
)

Boundary = Union[Limit, UnlimitedType]

validate_integer_type: Final = TypeValidator((int,))

UNLIMITED = UnlimitedType.UNLIMITED


class IntegerValidator:

    __slots__ = ("minimum", "maximum", "allow_bool")

    def __init__(self, minimum: Boundary, maximum: Boundary, allow_bool: bool) -> None:
        self.minimum = minimum
        self.maximum = maximum
        self.allow_bool = allow_bool

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"

    # noinspection PyTypeChecker
    def __call__(self, data: Any) -> Result[None, TestplatesError]:
        if (result := validate_integer_type(data)).is_failure:
            return Failure.from_result(result)

        if (result := validate_bool_type(data, self.allow_bool)).is_failure:
            return Failure.from_result(result)

        if (result := validate_boundaries(data, self.minimum, self.maximum)).is_failure:
            return Failure.from_result(result)

        return Success(None)


# noinspection PyTypeChecker
def validate_bool_type(data: int, allow_bool: bool, /) -> Result[None, TestplatesError]:
    if not allow_bool and isinstance(data, bool):
        return Failure(ProhibitedBoolValueError(data))

    return Success(None)


# noinspection PyTypeChecker
def validate_boundaries(
    data: int, minimum: Boundary, maximum: Boundary, /
) -> Result[None, TestplatesError]:
    if minimum is not UNLIMITED and not fits_minimum(data, minimum):
        return Failure(InvalidMinimumValueError(data, minimum))

    if maximum is not UNLIMITED and not fits_maximum(data, maximum):
        return Failure(InvalidMaximumValueError(data, maximum))

    return Success(None)
