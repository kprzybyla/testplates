__all__ = ["ranges_between"]

from typing import overload, Any, TypeVar, Generic, Optional

import testplates

from testplates.abc import Constraint
from testplates.boundaries import (
    get_minimum,
    get_maximum,
    fits_minimum,
    fits_maximum,
    check_boundaries,
)

_T = TypeVar("_T", int, float)


class RangesBetween(Generic[_T], Constraint):

    __slots__ = ("_minimum", "_maximum")

    def __init__(
        self,
        *,
        inclusive_minimum: Optional[_T] = None,
        inclusive_maximum: Optional[_T] = None,
        exclusive_minimum: Optional[_T] = None,
        exclusive_maximum: Optional[_T] = None,
    ) -> None:
        minimum = get_minimum(inclusive=inclusive_minimum, exclusive=exclusive_minimum)

        if isinstance(minimum, Exception):
            raise minimum

        maximum = get_maximum(inclusive=inclusive_maximum, exclusive=exclusive_maximum)

        if isinstance(maximum, Exception):
            raise maximum

        error = check_boundaries(minimum=minimum, maximum=maximum,)

        if error is not None:
            raise error

        self._minimum = minimum
        self._maximum = maximum

    def __repr__(self) -> str:
        boundaries = [
            repr(self._minimum),
            repr(self._maximum),
        ]

        return f"{testplates.__name__}.{ranges_between.__name__}({', '.join(boundaries)})"

    def __eq__(self, other: Any) -> bool:
        minimum_fits = fits_minimum(other, self._minimum)
        maximum_fits = fits_maximum(other, self._maximum)

        return minimum_fits and maximum_fits


@overload
def ranges_between(*, minimum: Optional[_T], maximum: Optional[_T]) -> RangesBetween[_T]:
    ...


@overload
def ranges_between(*, minimum: Optional[_T], exclusive_maximum: Optional[_T]) -> RangesBetween[_T]:
    ...


@overload
def ranges_between(*, exclusive_minimum: Optional[_T], maximum: Optional[_T]) -> RangesBetween[_T]:
    ...


@overload
def ranges_between(
    *, exclusive_minimum: Optional[_T], exclusive_maximum: Optional[_T]
) -> RangesBetween[_T]:
    ...


def ranges_between(
    *,
    minimum: Optional[_T] = None,
    maximum: Optional[_T] = None,
    exclusive_minimum: Optional[_T] = None,
    exclusive_maximum: Optional[_T] = None,
) -> RangesBetween[_T]:

    """
        Returns constraint object that matches any object with boundaries
        support that ranges between minimum and maximum boundaries values.

        :param minimum: inclusive minimum boundary value
        :param maximum: inclusive maximum boundary value
        :param exclusive_minimum: exclusive minimum boundary value
        :param exclusive_maximum: exclusive maximum boundary value
    """

    if (
        minimum is not None
        or maximum is not None
        or exclusive_minimum is not None
        or exclusive_maximum is not None
    ):
        return RangesBetween(
            inclusive_minimum=minimum,
            inclusive_maximum=maximum,
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )

    raise TypeError("ranges_between() missing 2 required keyword-only arguments")
