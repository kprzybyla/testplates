__all__ = ["any_number_validator", "integer_validator", "float_validator"]

from typing import overload, Any, TypeVar, Generic, Union, Optional, Final

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

_T = TypeVar("_T", bound=Union[int, float])

validate_any_number_type: Final = type_validator(int, float).value
validate_integer_type: Final = type_validator(int).value
validate_float_type: Final = type_validator(float).value


class AnyNumberValidator(Generic[_T]):

    __slots__ = ("minimum", "maximum", "allow_boolean")

    def __init__(self, minimum: Boundary[_T], maximum: Boundary[_T], allow_boolean: bool) -> None:
        self.minimum = minimum
        self.maximum = maximum
        self.allow_boolean = allow_boolean

    def __repr__(self) -> str:
        return f"{any_number_validator.__name__}()"

    def __call__(self, data: Any) -> Result[None, ValidationError]:
        if (result := validate_any_number_type(data)).is_error:
            return Failure.from_failure(result)

        if (result := validate_boolean_type(data, self.allow_boolean)).is_error:
            return Failure.from_failure(result)

        if (result := validate_boundaries(data, self.minimum, self.maximum)).is_error:
            return Failure.from_failure(result)

        return Success(None)


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

    def __call__(self, data: Any) -> Result[None, ValidationError]:
        if (result := validate_integer_type(data)).is_error:
            return Failure.from_failure(result)

        if (result := validate_boolean_type(data, self.allow_boolean)).is_error:
            return Failure.from_failure(result)

        if (result := validate_boundaries(data, self.minimum, self.maximum)).is_error:
            return Failure.from_failure(result)

        return Success(None)


class FloatValidator:

    __slots__ = ("minimum", "maximum")

    def __init__(self, minimum: Boundary[float], maximum: Boundary[float]) -> None:
        self.minimum = minimum
        self.maximum = maximum

    def __repr__(self) -> str:
        return f"{float_validator.__name__}()"

    def __call__(self, data: Any) -> Result[None, ValidationError]:
        if (result := validate_float_type(data)).is_error:
            return Failure.from_failure(result)

        if (result := validate_boundaries(data, self.minimum, self.maximum)).is_error:
            return Failure.from_failure(result)

        return Success(None)


@overload
def any_number_validator(
    *,
    minimum_value: Optional[Edge[_T]] = None,
    maximum_value: Optional[Edge[_T]] = None,
    allow_boolean: bool = False,
) -> Result[Validator, ValidationError]:
    ...


@overload
def any_number_validator(
    *,
    minimum_value: Optional[Edge[_T]] = None,
    exclusive_maximum_value: Optional[Edge[_T]] = None,
    allow_boolean: bool = False,
) -> Result[Validator, ValidationError]:
    ...


@overload
def any_number_validator(
    *,
    exclusive_minimum_value: Optional[Edge[_T]] = None,
    maximum_value: Optional[Edge[_T]] = None,
    allow_boolean: bool = False,
) -> Result[Validator, ValidationError]:
    ...


@overload
def any_number_validator(
    *,
    exclusive_minimum_value: Optional[Edge[_T]] = None,
    exclusive_maximum_value: Optional[Edge[_T]] = None,
    allow_boolean: bool = False,
) -> Result[Validator, ValidationError]:
    ...


def any_number_validator(
    *,
    minimum_value: Optional[Edge[_T]] = None,
    maximum_value: Optional[Edge[_T]] = None,
    exclusive_minimum_value: Optional[Edge[_T]] = None,
    exclusive_maximum_value: Optional[Edge[_T]] = None,
    allow_boolean: bool = False,
) -> Result[Validator, ValidationError]:
    boundaries = get_value_boundaries(
        inclusive_minimum=minimum_value,
        inclusive_maximum=maximum_value,
        exclusive_minimum=exclusive_minimum_value,
        exclusive_maximum=exclusive_maximum_value,
    )

    if boundaries.is_error:
        return Failure.from_failure(boundaries)

    minimum, maximum = boundaries.value

    return Success(AnyNumberValidator(minimum, maximum, allow_boolean))


@overload
def integer_validator(
    *,
    minimum_value: Optional[Edge[int]] = None,
    maximum_value: Optional[Edge[int]] = None,
    allow_boolean: bool = False,
) -> Result[Validator[int]]:
    ...


@overload
def integer_validator(
    *,
    minimum_value: Optional[Edge[int]] = None,
    exclusive_maximum_value: Optional[Edge[int]] = None,
    allow_boolean: bool = False,
) -> Result[Validator, ValidationError]:
    ...


@overload
def integer_validator(
    *,
    exclusive_minimum_value: Optional[Edge[int]] = None,
    maximum_value: Optional[Edge[int]] = None,
    allow_boolean: bool = False,
) -> Result[Validator, ValidationError]:
    ...


@overload
def integer_validator(
    *,
    exclusive_minimum_value: Optional[Edge[int]] = None,
    exclusive_maximum_value: Optional[Edge[int]] = None,
    allow_boolean: bool = False,
) -> Result[Validator, ValidationError]:
    ...


def integer_validator(
    *,
    minimum_value: Optional[Edge[int]] = None,
    maximum_value: Optional[Edge[int]] = None,
    exclusive_minimum_value: Optional[Edge[int]] = None,
    exclusive_maximum_value: Optional[Edge[int]] = None,
    allow_boolean: bool = False,
) -> Result[Validator, ValidationError]:
    boundaries = get_value_boundaries(
        inclusive_minimum=minimum_value,
        inclusive_maximum=maximum_value,
        exclusive_minimum=exclusive_minimum_value,
        exclusive_maximum=exclusive_maximum_value,
    )

    if boundaries.is_error:
        return Failure.from_failure(boundaries)

    minimum, maximum = boundaries.value

    return Success(IntegerValidator(minimum, maximum, allow_boolean))


@overload
def float_validator(
    *, minimum_value: Optional[Edge[float]] = None, maximum_value: Optional[Edge[float]] = None
) -> Result[Validator, ValidationError]:
    ...


@overload
def float_validator(
    *,
    minimum_value: Optional[Edge[float]] = None,
    exclusive_maximum_value: Optional[Edge[float]] = None,
) -> Result[Validator, ValidationError]:
    ...


@overload
def float_validator(
    *,
    exclusive_minimum_value: Optional[Edge[float]] = None,
    maximum_value: Optional[Edge[float]] = None,
) -> Result[Validator[float]]:
    ...


@overload
def float_validator(
    *,
    exclusive_minimum_value: Optional[Edge[float]] = None,
    exclusive_maximum_value: Optional[Edge[float]] = None,
) -> Result[Validator, ValidationError]:
    ...


def float_validator(
    *,
    minimum_value: Optional[Edge[float]] = None,
    maximum_value: Optional[Edge[float]] = None,
    exclusive_minimum_value: Optional[Edge[float]] = None,
    exclusive_maximum_value: Optional[Edge[float]] = None,
) -> Result[Validator, ValidationError]:
    boundaries = get_value_boundaries(
        inclusive_minimum=minimum_value,
        inclusive_maximum=maximum_value,
        exclusive_minimum=exclusive_minimum_value,
        exclusive_maximum=exclusive_maximum_value,
    )

    if boundaries.is_error:
        return Failure.from_failure(boundaries)

    minimum, maximum = boundaries.value

    return Success(FloatValidator(minimum, maximum))


def validate_boolean_type(
    data: Union[int, float], allow_boolean: bool, /
) -> Result[None, ValidationError]:
    if not allow_boolean and isinstance(data, bool):
        return Failure(ProhibitedBooleanValueError(data))

    return Success(None)


def validate_boundaries(
    data: _T, minimum: Boundary[_T], maximum: Boundary[_T], /
) -> Result[None, ValidationError]:
    if minimum is not UNLIMITED and not fits_minimum(data, minimum):
        return Failure(InvalidMinimumValueError(data, minimum))

    if maximum is not UNLIMITED and not fits_maximum(data, maximum):
        return Failure(InvalidMaximumValueError(data, maximum))

    return Success(None)
