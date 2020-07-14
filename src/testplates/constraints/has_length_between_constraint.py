__all__ = ["has_length_between"]

from typing import Any, Sized

import testplates

from testplates.abc import Constraint
from testplates.result import Success, Failure
from testplates.boundaries import get_length_boundaries, fits_minimum, fits_maximum, Edge, Boundary


class HasLengthBetween(Constraint):

    __slots__ = ("_minimum", "_maximum")

    def __init__(self, *, minimum: Boundary, maximum: Boundary) -> None:
        self._minimum = minimum
        self._maximum = maximum

    def __repr__(self) -> str:
        boundaries = [
            repr(self._minimum),
            repr(self._maximum),
        ]

        return f"{testplates.__name__}.{has_length_between.__name__}({', '.join(boundaries)})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Sized):
            return False

        length = len(other)

        minimum_fits = fits_minimum(length, self._minimum)
        maximum_fits = fits_maximum(length, self._maximum)

        return minimum_fits and maximum_fits


def has_length_between(*, minimum: Edge, maximum: Edge) -> HasLengthBetween:

    """
        Returns constraint object that matches any sized object
        that has length between minimum and maximum boundaries values.

        :param minimum: minimum length boundary value
        :param maximum: maximum length boundary value
    """

    result = get_length_boundaries(inclusive_minimum=minimum, inclusive_maximum=maximum)

    if result.is_failure:
        raise Failure.get_error(result)

    minimum_boundary, maximum_boundary = Success.get_value(result)

    return HasLengthBetween(minimum=minimum_boundary, maximum=maximum_boundary)
