__all__ = ["number_validator", "integer_validator", "float_validator"]

from typing import TypeVar, Callable, Optional

from testplates.constraints.boundaries import get_boundaries

from .type import type_validator
from .exceptions import (
    InvalidMinimumValueError,
    InvalidMaximumValueError,
    ProhibitedBooleanValueError,
)

_T = TypeVar("_T", int, float)

validate_number_type = type_validator(allowed_types=(int, float))
validate_integer_type = type_validator(allowed_types=int)
validate_float_type = type_validator(allowed_types=float)


def number_validator(
    *,
    validate_type: Callable[[_T], Optional[Exception]] = validate_number_type,
    minimum: Optional[_T] = None,
    maximum: Optional[_T] = None,
    exclusive_minimum: Optional[_T] = None,
    exclusive_maximum: Optional[_T] = None,
    allow_boolean: bool = False,
) -> Callable[[_T], Optional[Exception]]:
    minimum, maximum = get_boundaries(
        inclusive_minimum=minimum,
        inclusive_maximum=maximum,
        exclusive_minimum=exclusive_minimum,
        exclusive_maximum=exclusive_maximum,
    )

    def validate(data: _T) -> Optional[Exception]:
        if (error := validate_type(data)) is not None:
            return error

        if not allow_boolean and isinstance(data, bool):
            return ProhibitedBooleanValueError(data)

        if not minimum.fits(data):
            return InvalidMinimumValueError(data, minimum)

        if not maximum.fits(data):
            return InvalidMaximumValueError(data, maximum)

    return validate


def integer_validator(
    *,
    minimum: Optional[int] = None,
    maximum: Optional[int] = None,
    exclusive_minimum: Optional[int] = None,
    exclusive_maximum: Optional[int] = None,
    allow_boolean: bool = False,
) -> Callable[[int], Optional[Exception]]:
    validate_integer = number_validator(
        validate_type=validate_integer_type,
        minimum=minimum,
        maximum=maximum,
        exclusive_minimum=exclusive_minimum,
        exclusive_maximum=exclusive_maximum,
        allow_boolean=allow_boolean,
    )

    def validate(data: int) -> Optional[Exception]:
        return validate_integer(data)

    return validate


def float_validator(
    *,
    minimum: Optional[float] = None,
    maximum: Optional[float] = None,
    exclusive_minimum: Optional[float] = None,
    exclusive_maximum: Optional[float] = None,
    allow_boolean: bool = False,
) -> Callable[[float], Optional[Exception]]:
    validate_float = number_validator(
        validate_type=validate_float_type,
        minimum=minimum,
        maximum=maximum,
        exclusive_minimum=exclusive_minimum,
        exclusive_maximum=exclusive_maximum,
        allow_boolean=allow_boolean,
    )

    def validate(data: float) -> Optional[Exception]:
        return validate_float(data)

    return validate
