__all__ = ["HasLengthBetween"]

from typing import Any, Union, Sized

import testplates

from testplates.impl.abc import Constraint
from testplates.impl.base import fits_minimum, fits_maximum, Limit, UnlimitedType

Boundary = Union[Limit, UnlimitedType]


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

        return f"{testplates.__name__}.{type(self).__name__}({', '.join(boundaries)})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Sized):
            return False

        length = len(other)

        minimum_fits = fits_minimum(length, self._minimum)
        maximum_fits = fits_maximum(length, self._maximum)

        return minimum_fits and maximum_fits
