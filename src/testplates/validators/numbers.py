__all__ = ["any_number_validator", "integer_validator", "float_validator"]

from typing import overload, TypeVar, Union, Callable, Optional, Final

from testplates.boundaries import (
    get_minimum,
    get_maximum,
    fits_minimum,
    fits_maximum,
    check_boundaries,
    Boundary,
    UNLIMITED,
)

from .type import type_validator
from .utils import Result, Validator
from .exceptions import (
    InvalidMinimumValueError,
    InvalidMaximumValueError,
    ProhibitedBooleanValueError,
)

_T = TypeVar("_T", bound=Union[int, float])

validate_any_number_type: Final = type_validator(allowed_types=(int, float))
validate_integer_type: Final = type_validator(allowed_types=int)
validate_float_type: Final = type_validator(allowed_types=float)


@overload
def any_number_validator(
    *,
    minimum_value: Optional[_T] = None,
    maximum_value: Optional[_T] = None,
    allow_boolean: bool = False,
) -> Result[Validator[_T]]:
    ...


@overload
def any_number_validator(
    *,
    minimum_value: Optional[_T] = None,
    exclusive_maximum_value: Optional[_T] = None,
    allow_boolean: bool = False,
) -> Result[Validator[_T]]:
    ...


@overload
def any_number_validator(
    *,
    exclusive_minimum_value: Optional[_T] = None,
    maximum_value: Optional[_T] = None,
    allow_boolean: bool = False,
) -> Result[Validator[_T]]:
    ...


@overload
def any_number_validator(
    *,
    exclusive_minimum_value: Optional[_T] = None,
    exclusive_maximum_value: Optional[_T] = None,
    allow_boolean: bool = False,
) -> Result[Validator[_T]]:
    ...


def any_number_validator(
    *,
    minimum_value: Optional[_T] = None,
    maximum_value: Optional[_T] = None,
    exclusive_minimum_value: Optional[_T] = None,
    exclusive_maximum_value: Optional[_T] = None,
    allow_boolean: bool = False,
) -> Result[Validator[_T]]:
    minimum = get_minimum(inclusive=minimum_value, exclusive=exclusive_minimum_value)

    if isinstance(minimum, Exception):
        return minimum

    maximum = get_maximum(inclusive=maximum_value, exclusive=exclusive_maximum_value)

    if isinstance(maximum, Exception):
        return maximum

    outcome = check_boundaries(minimum=minimum, maximum=maximum)

    if outcome is not None:
        return outcome

    def validate(data: _T) -> Optional[Exception]:
        if (error := validate_any_number_type(data)) is not None:
            return error

        if (error := validate_any_number_boolean_type(data, allow_boolean)) is not None:
            return error

        if (error := validate_any_number_boundaries(data, minimum, maximum)) is not None:
            return error

        return None

    return validate


@overload
def integer_validator(
    *,
    minimum_value: Optional[int] = None,
    maximum_value: Optional[int] = None,
    allow_boolean: bool = False,
) -> Result[Validator[int]]:
    ...


@overload
def integer_validator(
    *,
    minimum_value: Optional[int] = None,
    exclusive_maximum_value: Optional[int] = None,
    allow_boolean: bool = False,
) -> Result[Validator[int]]:
    ...


@overload
def integer_validator(
    *,
    exclusive_minimum_value: Optional[int] = None,
    maximum_value: Optional[int] = None,
    allow_boolean: bool = False,
) -> Callable[[int], Optional[Exception]]:
    ...


@overload
def integer_validator(
    *,
    exclusive_minimum_value: Optional[int] = None,
    exclusive_maximum_value: Optional[int] = None,
    allow_boolean: bool = False,
) -> Result[Validator[int]]:
    ...


def integer_validator(
    *,
    minimum_value: Optional[int] = None,
    maximum_value: Optional[int] = None,
    exclusive_minimum_value: Optional[int] = None,
    exclusive_maximum_value: Optional[int] = None,
    allow_boolean: bool = False,
) -> Result[Validator[int]]:
    minimum = get_minimum(inclusive=minimum_value, exclusive=exclusive_minimum_value)

    if isinstance(minimum, Exception):
        return minimum

    maximum = get_maximum(inclusive=maximum_value, exclusive=exclusive_maximum_value)

    if isinstance(maximum, Exception):
        return maximum

    outcome = check_boundaries(minimum=minimum, maximum=maximum,)

    if outcome is not None:
        return outcome

    def validate(data: int) -> Optional[Exception]:
        if (error := validate_integer_type(data)) is not None:
            return error

        if (error := validate_any_number_boolean_type(data, allow_boolean)) is not None:
            return error

        if (error := validate_any_number_boundaries(data, minimum, maximum)) is not None:
            return error

        return None

    return validate


@overload
def float_validator(
    *, minimum_value: Optional[float] = None, maximum_value: Optional[float] = None
) -> Result[Validator[float]]:
    ...


@overload
def float_validator(
    *, minimum_value: Optional[float] = None, exclusive_maximum_value: Optional[float] = None
) -> Result[Validator[float]]:
    ...


@overload
def float_validator(
    *, exclusive_minimum_value: Optional[float] = None, maximum_value: Optional[float] = None
) -> Result[Validator[float]]:
    ...


@overload
def float_validator(
    *,
    exclusive_minimum_value: Optional[float] = None,
    exclusive_maximum_value: Optional[float] = None,
) -> Result[Validator[float]]:
    ...


def float_validator(
    *,
    minimum_value: Optional[float] = None,
    maximum_value: Optional[float] = None,
    exclusive_minimum_value: Optional[float] = None,
    exclusive_maximum_value: Optional[float] = None,
) -> Result[Validator[float]]:
    minimum = get_minimum(inclusive=minimum_value, exclusive=exclusive_minimum_value)

    if isinstance(minimum, Exception):
        return minimum

    maximum = get_maximum(inclusive=maximum_value, exclusive=exclusive_maximum_value)

    if isinstance(maximum, Exception):
        return maximum

    outcome = check_boundaries(minimum=minimum, maximum=maximum,)

    if outcome is not None:
        return outcome

    def validate(data: float) -> Optional[Exception]:
        if (error := validate_float_type(data)) is not None:
            return error

        if (error := validate_any_number_boundaries(data, minimum, maximum)) is not None:
            return error

        return None

    return validate


def validate_any_number_boolean_type(
    data: Union[int, float], allow_boolean: bool, /
) -> Optional[Exception]:
    if not allow_boolean and isinstance(data, bool):
        return ProhibitedBooleanValueError(data)

    return None


def validate_any_number_boundaries(
    data: _T, minimum: Boundary[_T], maximum: Boundary[_T], /
) -> Optional[Exception]:
    if minimum is not UNLIMITED and not fits_minimum(data, minimum):
        return InvalidMinimumValueError(data, minimum)

    if maximum is not UNLIMITED and not fits_maximum(data, maximum):
        return InvalidMaximumValueError(data, maximum)

    return None
