__all__ = ["HasLengthBetween"]

from typing import Any, Union, Sized

import testplates

from testplates.impl.base import fits_minimum_length, fits_maximum_length, Limit, UnlimitedType

Boundary = Union[Limit, UnlimitedType]


class HasLengthBetween:

    __slots__ = ("_minimum_length", "_maximum_length")

    def __init__(self, *, minimum_length: Boundary, maximum_length: Boundary) -> None:
        self._minimum_length = minimum_length
        self._maximum_length = maximum_length

    def __repr__(self) -> str:
        boundaries = [
            repr(self._minimum_length),
            repr(self._maximum_length),
        ]

        return f"{testplates.__name__}.has_size_between({', '.join(boundaries)})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Sized):
            return False

        minimum_fits = fits_minimum_length(other, self._minimum_length)
        maximum_fits = fits_maximum_length(other, self._maximum_length)

        return minimum_fits and maximum_fits
