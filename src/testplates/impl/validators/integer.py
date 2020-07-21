__all__ = ["IntegerValidator"]

from typing import Any, Union, Final

from testplates.impl.base import Result, Success, Failure
from testplates.impl.base import fits_minimum, fits_maximum, Limit, UnlimitedType

from .type import TypeValidator
from .exceptions import (
    ValidationError,
    InvalidMinimumValueError,
    InvalidMaximumValueError,
    ProhibitedBooleanValueError,
)

Boundary = Union[Limit, UnlimitedType]

validate_integer_type: Final = TypeValidator((int,))

UNLIMITED = UnlimitedType.UNLIMITED


class IntegerValidator:

    __slots__ = ("minimum", "maximum", "allow_boolean")

    def __init__(self, minimum: Boundary, maximum: Boundary, allow_boolean: bool) -> None:
        self.minimum = minimum
        self.maximum = maximum
        self.allow_boolean = allow_boolean

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"

    # noinspection PyTypeChecker
    def __call__(self, data: Any) -> Result[None, ValidationError]:
        if (result := validate_integer_type(data)).is_failure:
            return Failure.from_result(result)

        if (result := validate_boolean_type(data, self.allow_boolean)).is_failure:
            return Failure.from_result(result)

        if (result := validate_boundaries(data, self.minimum, self.maximum)).is_failure:
            return Failure.from_result(result)

        return Success(None)


# noinspection PyTypeChecker
def validate_boolean_type(data: int, allow_boolean: bool, /) -> Result[None, ValidationError]:
    if not allow_boolean and isinstance(data, bool):
        return Failure(ProhibitedBooleanValueError(data))

    return Success(None)


# noinspection PyTypeChecker
def validate_boundaries(
    data: int, minimum: Boundary, maximum: Boundary, /
) -> Result[None, ValidationError]:
    if minimum is not UNLIMITED and not fits_minimum(data, minimum):
        return Failure(InvalidMinimumValueError(data, minimum))

    if maximum is not UNLIMITED and not fits_maximum(data, maximum):
        return Failure(InvalidMaximumValueError(data, maximum))

    return Success(None)
