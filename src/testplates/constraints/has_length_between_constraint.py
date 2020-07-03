__all__ = ["has_length_between"]

from typing import Any, Sized

import testplates

from testplates.abc import Constraint
from testplates.boundaries import get_length_boundaries, fits_minimum, fits_maximum, Edge


class HasLengthBetween(Constraint):

    __slots__ = ("_minimum", "_maximum")

    def __init__(self, *, minimum_length: Edge[int], maximum_length: Edge[int]) -> None:
        result = get_length_boundaries(
            inclusive_minimum=minimum_length, inclusive_maximum=maximum_length
        )

        if result.is_failure:
            raise result.error

        self._minimum, self._maximum = result.value

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


def has_length_between(*, minimum: Edge[int], maximum: Edge[int]) -> HasLengthBetween:

    """
        Returns constraint object that matches any sized object
        that has length between minimum and maximum boundaries values.

        :param minimum: minimum length boundary value
        :param maximum: maximum length boundary value
    """

    return HasLengthBetween(minimum_length=minimum, maximum_length=maximum)
