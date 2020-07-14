__all__ = ["ranges_between"]

from typing import overload, Any, Optional

import testplates

from testplates.abc import Constraint
from testplates.result import Success, Failure
from testplates.boundaries import get_value_boundaries, fits_minimum, fits_maximum, Edge, Boundary


class RangesBetween(Constraint):

    __slots__ = ("_minimum", "_maximum")

    def __init__(self, *, minimum: Boundary, maximum: Boundary) -> None:
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
def ranges_between(*, minimum: Optional[Edge], maximum: Optional[Edge]) -> RangesBetween:
    ...


@overload
def ranges_between(*, minimum: Optional[Edge], exclusive_maximum: Optional[Edge]) -> RangesBetween:
    ...


@overload
def ranges_between(*, exclusive_minimum: Optional[Edge], maximum: Optional[Edge]) -> RangesBetween:
    ...


@overload
def ranges_between(
    *, exclusive_minimum: Optional[Edge], exclusive_maximum: Optional[Edge]
) -> RangesBetween:
    ...


def ranges_between(
    *,
    minimum: Optional[Edge] = None,
    maximum: Optional[Edge] = None,
    exclusive_minimum: Optional[Edge] = None,
    exclusive_maximum: Optional[Edge] = None,
) -> RangesBetween:

    """
        Returns constraint object that matches any object with boundaries
        support that ranges between minimum and maximum boundaries values.

        :param minimum: inclusive minimum boundary value
        :param maximum: inclusive maximum boundary value
        :param exclusive_minimum: exclusive minimum boundary value
        :param exclusive_maximum: exclusive maximum boundary value
    """

    result = get_value_boundaries(
        inclusive_minimum=minimum,
        inclusive_maximum=maximum,
        exclusive_minimum=exclusive_minimum,
        exclusive_maximum=exclusive_maximum,
    )

    if result.is_failure:
        raise Failure.get_error(result)

    minimum_boundary, maximum_boundary = Success.get_value(result)

    return RangesBetween(minimum=minimum_boundary, maximum=maximum_boundary)
