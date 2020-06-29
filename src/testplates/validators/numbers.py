__all__ = ["any_number_validator", "integer_validator", "float_validator"]

from typing import overload, TypeVar, Union, Callable, Optional, Final

from testplates.result import Result, Success, Failure
from testplates.boundaries import (
    get_value_boundaries,
    fits_minimum,
    fits_maximum,
    Boundary,
    UNLIMITED,
)

from .type import type_validator
from .utils import Validator
from .exceptions import (
    InvalidMinimumValueError,
    InvalidMaximumValueError,
    ProhibitedBooleanValueError,
)

_T = TypeVar("_T", bound=Union[int, float])

validate_any_number_type: Final = type_validator(allowed_types=(int, float)).value
validate_integer_type: Final = type_validator(allowed_types=int).value
validate_float_type: Final = type_validator(allowed_types=float).value


@overload
def any_number_validator(
    *,
    minimum_value: Optional[Boundary[_T]] = None,
    maximum_value: Optional[Boundary[_T]] = None,
    allow_boolean: bool = False,
) -> Result[Validator[_T]]:
    ...


@overload
def any_number_validator(
    *,
    minimum_value: Optional[Boundary[_T]] = None,
    exclusive_maximum_value: Optional[Boundary[_T]] = None,
    allow_boolean: bool = False,
) -> Result[Validator[_T]]:
    ...


@overload
def any_number_validator(
    *,
    exclusive_minimum_value: Optional[Boundary[_T]] = None,
    maximum_value: Optional[Boundary[_T]] = None,
    allow_boolean: bool = False,
) -> Result[Validator[_T]]:
    ...


@overload
def any_number_validator(
    *,
    exclusive_minimum_value: Optional[Boundary[_T]] = None,
    exclusive_maximum_value: Optional[Boundary[_T]] = None,
    allow_boolean: bool = False,
) -> Result[Validator[_T]]:
    ...


def any_number_validator(
    *,
    minimum_value: Optional[Boundary[_T]] = None,
    maximum_value: Optional[Boundary[_T]] = None,
    exclusive_minimum_value: Optional[Boundary[_T]] = None,
    exclusive_maximum_value: Optional[Boundary[_T]] = None,
    allow_boolean: bool = False,
) -> Result[Validator[_T]]:
    boundaries = get_value_boundaries(
        inclusive_minimum=minimum_value,
        inclusive_maximum=maximum_value,
        exclusive_minimum=exclusive_minimum_value,
        exclusive_maximum=exclusive_maximum_value,
    )

    if boundaries.is_error:
        return Failure.from_failure(boundaries)

    minimum, maximum = boundaries.value

    def validate(data: _T) -> Result[None]:
        if (result := validate_any_number_type(data)).is_error:
            return Failure.from_failure(result)

        if (result := validate_any_number_boolean_type(data, allow_boolean)).is_error:
            return Failure.from_failure(result)

        if (result := validate_any_number_boundaries(data, minimum, maximum)).is_error:
            return Failure.from_failure(result)

        return Success(None)

    return Success(validate)


@overload
def integer_validator(
    *,
    minimum_value: Optional[Boundary[int]] = None,
    maximum_value: Optional[Boundary[int]] = None,
    allow_boolean: bool = False,
) -> Result[Validator[int]]:
    ...


@overload
def integer_validator(
    *,
    minimum_value: Optional[Boundary[int]] = None,
    exclusive_maximum_value: Optional[Boundary[int]] = None,
    allow_boolean: bool = False,
) -> Result[Validator[int]]:
    ...


@overload
def integer_validator(
    *,
    exclusive_minimum_value: Optional[Boundary[int]] = None,
    maximum_value: Optional[Boundary[int]] = None,
    allow_boolean: bool = False,
) -> Callable[[int], Optional[Exception]]:
    ...


@overload
def integer_validator(
    *,
    exclusive_minimum_value: Optional[Boundary[int]] = None,
    exclusive_maximum_value: Optional[Boundary[int]] = None,
    allow_boolean: bool = False,
) -> Result[Validator[int]]:
    ...


def integer_validator(
    *,
    minimum_value: Optional[Boundary[int]] = None,
    maximum_value: Optional[Boundary[int]] = None,
    exclusive_minimum_value: Optional[Boundary[int]] = None,
    exclusive_maximum_value: Optional[Boundary[int]] = None,
    allow_boolean: bool = False,
) -> Result[Validator[int]]:
    boundaries = get_value_boundaries(
        inclusive_minimum=minimum_value,
        inclusive_maximum=maximum_value,
        exclusive_minimum=exclusive_minimum_value,
        exclusive_maximum=exclusive_maximum_value,
    )

    if boundaries.is_error:
        return Failure.from_failure(boundaries)

    minimum, maximum = boundaries.value

    def validate(data: int) -> Result[None]:
        if (result := validate_integer_type(data)).is_error:
            return Failure.from_failure(result)

        if (result := validate_any_number_boolean_type(data, allow_boolean)).is_error:
            return Failure.from_failure(result)

        if (result := validate_any_number_boundaries(data, minimum, maximum)).is_error:
            return Failure.from_failure(result)

        return Success(None)

    return Success(validate)


@overload
def float_validator(
    *,
    minimum_value: Optional[Boundary[float]] = None,
    maximum_value: Optional[Boundary[float]] = None,
) -> Result[Validator[float]]:
    ...


@overload
def float_validator(
    *,
    minimum_value: Optional[Boundary[float]] = None,
    exclusive_maximum_value: Optional[Boundary[float]] = None,
) -> Result[Validator[float]]:
    ...


@overload
def float_validator(
    *,
    exclusive_minimum_value: Optional[Boundary[float]] = None,
    maximum_value: Optional[Boundary[float]] = None,
) -> Result[Validator[float]]:
    ...


@overload
def float_validator(
    *,
    exclusive_minimum_value: Optional[Boundary[float]] = None,
    exclusive_maximum_value: Optional[Boundary[float]] = None,
) -> Result[Validator[float]]:
    ...


def float_validator(
    *,
    minimum_value: Optional[Boundary[float]] = None,
    maximum_value: Optional[Boundary[float]] = None,
    exclusive_minimum_value: Optional[Boundary[float]] = None,
    exclusive_maximum_value: Optional[Boundary[float]] = None,
) -> Result[Validator[float]]:
    boundaries = get_value_boundaries(
        inclusive_minimum=minimum_value,
        inclusive_maximum=maximum_value,
        exclusive_minimum=exclusive_minimum_value,
        exclusive_maximum=exclusive_maximum_value,
    )

    if boundaries.is_error:
        return Failure.from_failure(boundaries)

    minimum, maximum = boundaries.value

    def validate(data: float) -> Result[None]:
        if (result := validate_float_type(data)).is_error:
            return Failure.from_failure(result)

        if (result := validate_any_number_boundaries(data, minimum, maximum)).is_error:
            return Failure.from_failure(result)

        return Success(None)

    return Success(validate)


def validate_any_number_boolean_type(
    data: Union[int, float], allow_boolean: bool, /
) -> Result[None]:
    if not allow_boolean and isinstance(data, bool):
        return Failure(ProhibitedBooleanValueError(data))

    return Success(None)


def validate_any_number_boundaries(
    data: _T, minimum: Boundary[_T], maximum: Boundary[_T], /
) -> Result[None]:
    if minimum is not UNLIMITED and not fits_minimum(data, minimum):
        return Failure(InvalidMinimumValueError(data, minimum))

    if maximum is not UNLIMITED and not fits_maximum(data, maximum):
        return Failure(InvalidMaximumValueError(data, maximum))

    return Success(None)
