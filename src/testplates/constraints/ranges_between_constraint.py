__all__ = ["ranges_between"]

from typing import overload, Any, TypeVar, Generic, Optional

import testplates

from testplates.abc import Constraint
from testplates.boundaries import get_value_boundaries, fits_minimum, fits_maximum, Edge

_T = TypeVar("_T", int, float)


class RangesBetween(Generic[_T], Constraint):

    __slots__ = ("_minimum", "_maximum")

    def __init__(
        self,
        *,
        inclusive_minimum: Optional[Edge[_T]] = None,
        inclusive_maximum: Optional[Edge[_T]] = None,
        exclusive_minimum: Optional[Edge[_T]] = None,
        exclusive_maximum: Optional[Edge[_T]] = None,
    ) -> None:
        result = get_value_boundaries(
            inclusive_minimum=inclusive_minimum,
            inclusive_maximum=inclusive_maximum,
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )

        if result.is_failure:
            raise result.error

        self._minimum, self._maximum = result.value

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
def ranges_between(
    *, minimum: Optional[Edge[_T]], maximum: Optional[Edge[_T]]
) -> RangesBetween[_T]:
    ...


@overload
def ranges_between(
    *, minimum: Optional[Edge[_T]], exclusive_maximum: Optional[Edge[_T]]
) -> RangesBetween[_T]:
    ...


@overload
def ranges_between(
    *, exclusive_minimum: Optional[Edge[_T]], maximum: Optional[Edge[_T]]
) -> RangesBetween[_T]:
    ...


@overload
def ranges_between(
    *, exclusive_minimum: Optional[Edge[_T]], exclusive_maximum: Optional[Edge[_T]]
) -> RangesBetween[_T]:
    ...


def ranges_between(
    *,
    minimum: Optional[Edge[_T]] = None,
    maximum: Optional[Edge[_T]] = None,
    exclusive_minimum: Optional[Edge[_T]] = None,
    exclusive_maximum: Optional[Edge[_T]] = None,
) -> RangesBetween[_T]:

    """
        Returns constraint object that matches any object with boundaries
        support that ranges between minimum and maximum boundaries values.

        :param minimum: inclusive minimum boundary value
        :param maximum: inclusive maximum boundary value
        :param exclusive_minimum: exclusive minimum boundary value
        :param exclusive_maximum: exclusive maximum boundary value
    """

    return RangesBetween(
        inclusive_minimum=minimum,
        inclusive_maximum=maximum,
        exclusive_minimum=exclusive_minimum,
        exclusive_maximum=exclusive_maximum,
    )
