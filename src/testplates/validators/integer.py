__all__ = ["integer_validator"]

from typing import overload, Any, Union, Optional, Final

from testplates.result import Result, Success, Failure
from testplates.boundaries import (
    get_value_boundaries,
    fits_minimum,
    fits_maximum,
    Edge,
    Boundary,
    UNLIMITED,
)

from .utils import Validator
from .type import type_validator
from .exceptions import (
    ValidationError,
    InvalidMinimumValueError,
    InvalidMaximumValueError,
    ProhibitedBooleanValueError,
)

validate_integer_type: Final = Success.get_value(type_validator(int))


class IntegerValidator:

    __slots__ = ("minimum", "maximum", "allow_boolean")

    def __init__(
        self, minimum: Boundary[int], maximum: Boundary[int], allow_boolean: bool
    ) -> None:
        self.minimum = minimum
        self.maximum = maximum
        self.allow_boolean = allow_boolean

    def __repr__(self) -> str:
        return f"{integer_validator.__name__}()"

    # noinspection PyTypeChecker
    def __call__(self, data: Any) -> Result[None, ValidationError]:
        if (result := validate_integer_type(data)).is_failure:
            return Failure.from_result(result)

        if (result := validate_boolean_type(data, self.allow_boolean)).is_failure:
            return Failure.from_result(result)

        if (result := validate_boundaries(data, self.minimum, self.maximum)).is_failure:
            return Failure.from_result(result)

        return Success(None)


@overload
def integer_validator(
    *,
    minimum: Optional[Edge[int]] = None,
    maximum: Optional[Edge[int]] = None,
    allow_boolean: bool = False,
) -> Result[Validator, ValidationError]:
    ...


@overload
def integer_validator(
    *,
    minimum: Optional[Edge[int]] = None,
    exclusive_maximum: Optional[Edge[int]] = None,
    allow_boolean: bool = False,
) -> Result[Validator, ValidationError]:
    ...


@overload
def integer_validator(
    *,
    exclusive_minimum: Optional[Edge[int]] = None,
    maximum: Optional[Edge[int]] = None,
    allow_boolean: bool = False,
) -> Result[Validator, ValidationError]:
    ...


@overload
def integer_validator(
    *,
    exclusive_minimum: Optional[Edge[int]] = None,
    exclusive_maximum: Optional[Edge[int]] = None,
    allow_boolean: bool = False,
) -> Result[Validator, ValidationError]:
    ...


# noinspection PyTypeChecker
def integer_validator(
    *,
    minimum: Optional[Edge[int]] = None,
    maximum: Optional[Edge[int]] = None,
    exclusive_minimum: Optional[Edge[int]] = None,
    exclusive_maximum: Optional[Edge[int]] = None,
    allow_boolean: bool = False,
) -> Result[Validator, ValidationError]:
    result = get_value_boundaries(
        inclusive_minimum=minimum,
        inclusive_maximum=maximum,
        exclusive_minimum=exclusive_minimum,
        exclusive_maximum=exclusive_maximum,
    )

    if result.is_failure:
        return Failure.from_result(result)

    minimum, maximum = Success.get_value(result)

    return Success(IntegerValidator(minimum, maximum, allow_boolean))


# noinspection PyTypeChecker
def validate_boolean_type(
    data: Union[int, float], allow_boolean: bool, /
) -> Result[None, ValidationError]:
    if not allow_boolean and isinstance(data, bool):
        return Failure(ProhibitedBooleanValueError(data))

    return Success(None)


# noinspection PyTypeChecker
def validate_boundaries(
    data: int, minimum: Boundary[int], maximum: Boundary[int], /
) -> Result[None, ValidationError]:
    if minimum is not UNLIMITED and not fits_minimum(data, minimum):
        return Failure(InvalidMinimumValueError(data, minimum))

    if maximum is not UNLIMITED and not fits_maximum(data, maximum):
        return Failure(InvalidMaximumValueError(data, maximum))

    return Success(None)
