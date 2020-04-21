__all__ = ["Number", "Integer", "Float"]

from typing import Type, TypeVar, Generic, Optional

from testplates.constraints.boundaries import get_boundaries

from .base_validator import BaseValidator
from .exceptions import (
    InvalidMinimumValueError,
    InvalidMaximumValueError,
    ProhibitedBooleanValueError,
)

_T = TypeVar("_T", int, float)


class Number(BaseValidator[_T], Generic[_T]):

    __slots__ = ("_minimum", "_maximum", "_allow_boolean")

    def __init__(
        self,
        *,
        minimum: Optional[_T] = None,
        maximum: Optional[_T] = None,
        exclusive_minimum: Optional[_T] = None,
        exclusive_maximum: Optional[_T] = None,
        allow_boolean: bool = False,
    ) -> None:
        minimum, maximum = get_boundaries(
            inclusive_minimum=minimum,
            inclusive_maximum=maximum,
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )

        self._minimum = minimum
        self._maximum = maximum
        self._allow_boolean = allow_boolean

    @property
    def allowed_types(self) -> Type[_T]:
        return int, float

    def validate(self, data: _T) -> None:
        super().validate(data)

        if not self._allow_boolean and isinstance(data, bool):
            raise ProhibitedBooleanValueError(data)

        if not self._minimum.fits(data):
            raise InvalidMinimumValueError(data, self._minimum)

        if not self._maximum.fits(data):
            raise InvalidMaximumValueError(data, self._maximum)


class Integer(Number[int]):

    __slots__ = ()

    @property
    def allowed_types(self) -> Type[int]:
        return int


class Float(Number[float]):

    __slots__ = ()

    @property
    def allowed_types(self) -> Type[float]:
        return float
