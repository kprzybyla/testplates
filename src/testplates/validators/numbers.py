__all__ = ["any_number_validator", "integer_validator", "float_validator"]

from typing import overload, TypeVar, Callable, Optional, Final

from testplates.boundaries import get_boundaries

from .type import type_validator
from .exceptions import (
    InvalidMinimumValueError,
    InvalidMaximumValueError,
    ProhibitedBooleanValueError,
)

_T = TypeVar("_T", int, float)

validate_any_number_type: Final = type_validator(allowed_types=(int, float))
validate_integer_type: Final = type_validator(allowed_types=int)
validate_float_type: Final = type_validator(allowed_types=float)


@overload
def any_number_validator(
    *,
    minimum_value: Optional[_T] = None,
    maximum_value: Optional[_T] = None,
    allow_boolean: bool = False,
) -> Callable[[_T], Optional[Exception]]:
    ...


@overload
def any_number_validator(
    *,
    minimum_value: Optional[_T] = None,
    exclusive_maximum_value: Optional[_T] = None,
    allow_boolean: bool = False,
) -> Callable[[_T], Optional[Exception]]:
    ...


@overload
def any_number_validator(
    *,
    exclusive_minimum_value: Optional[_T] = None,
    maximum_value: Optional[_T] = None,
    allow_boolean: bool = False,
) -> Callable[[_T], Optional[Exception]]:
    ...


@overload
def any_number_validator(
    *,
    exclusive_minimum_value: Optional[_T] = None,
    exclusive_maximum_value: Optional[_T] = None,
    allow_boolean: bool = False,
) -> Callable[[_T], Optional[Exception]]:
    ...


def any_number_validator(  # type: ignore
    *,
    minimum_value: Optional[_T] = None,
    maximum_value: Optional[_T] = None,
    exclusive_minimum_value: Optional[_T] = None,
    exclusive_maximum_value: Optional[_T] = None,
    allow_boolean: bool = False,
) -> Callable[[_T], Optional[Exception]]:
    minimum, maximum = get_boundaries(
        inclusive_minimum=minimum_value,
        inclusive_maximum=maximum_value,
        exclusive_minimum=exclusive_minimum_value,
        exclusive_maximum=exclusive_maximum_value,
    )

    def validate(data: _T) -> Optional[Exception]:
        if (error := validate_any_number_type(data)) is not None:
            return error  # type: ignore

        if not allow_boolean and isinstance(data, bool):
            return ProhibitedBooleanValueError(data)

        if not minimum.fits(data):
            return InvalidMinimumValueError(data, minimum)

        if not maximum.fits(data):
            return InvalidMaximumValueError(data, maximum)

        return None

    return validate


@overload
def integer_validator(
    *,
    minimum_value: Optional[int] = None,
    maximum_value: Optional[int] = None,
    allow_boolean: bool = False,
) -> Callable[[int], Optional[Exception]]:
    ...


@overload
def integer_validator(
    *,
    minimum_value: Optional[int] = None,
    exclusive_maximum_value: Optional[int] = None,
    allow_boolean: bool = False,
) -> Callable[[int], Optional[Exception]]:
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
) -> Callable[[int], Optional[Exception]]:
    ...


# noinspection PyArgumentList
def integer_validator(
    *,
    minimum_value: Optional[int] = None,
    maximum_value: Optional[int] = None,
    exclusive_minimum_value: Optional[int] = None,
    exclusive_maximum_value: Optional[int] = None,
    allow_boolean: bool = False,
) -> Callable[[int], Optional[Exception]]:
    validate_integer: Callable[[int], Optional[Exception]] = any_number_validator(
        minimum_value=minimum_value,
        maximum_value=maximum_value,
        exclusive_minimum_value=exclusive_minimum_value,
        exclusive_maximum_value=exclusive_maximum_value,
        allow_boolean=allow_boolean,
    )  # type: ignore

    def validate(data: int) -> Optional[Exception]:
        if (error := validate_integer_type(data)) is not None:
            return error

        return validate_integer(data)

    return validate


@overload
def float_validator(
    *, minimum_value: Optional[float] = None, maximum_value: Optional[float] = None
) -> Callable[[float], Optional[Exception]]:
    ...


@overload
def float_validator(
    *, minimum_value: Optional[float] = None, exclusive_maximum_value: Optional[float] = None
) -> Callable[[float], Optional[Exception]]:
    ...


@overload
def float_validator(
    *, exclusive_minimum_value: Optional[float] = None, maximum_value: Optional[float] = None
) -> Callable[[float], Optional[Exception]]:
    ...


@overload
def float_validator(
    *,
    exclusive_minimum_value: Optional[float] = None,
    exclusive_maximum_value: Optional[float] = None,
) -> Callable[[float], Optional[Exception]]:
    ...


# noinspection PyArgumentList
def float_validator(
    *,
    minimum_value: Optional[float] = None,
    maximum_value: Optional[float] = None,
    exclusive_minimum_value: Optional[float] = None,
    exclusive_maximum_value: Optional[float] = None,
) -> Callable[[float], Optional[Exception]]:
    validate_float: Callable[[float], Optional[Exception]] = any_number_validator(
        minimum_value=minimum_value,
        maximum_value=maximum_value,
        exclusive_minimum_value=exclusive_minimum_value,
        exclusive_maximum_value=exclusive_maximum_value,
        allow_boolean=False,
    )  # type: ignore

    def validate(data: float) -> Optional[Exception]:
        if (error := validate_float_type(data)) is not None:
            return error

        return validate_float(data)

    return validate
