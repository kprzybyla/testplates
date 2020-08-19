__all__ = ["RangesBetween"]

from typing import Any, Union

import testplates

from testplates.impl.base import fits_minimum_value, fits_maximum_value, Limit, UnlimitedType

Boundary = Union[Limit, UnlimitedType]


class RangesBetween:

    __slots__ = ("minimum_value", "maximum_value")

    def __init__(self, *, minimum_value: Boundary, maximum_value: Boundary) -> None:
        self.minimum_value = minimum_value
        self.maximum_value = maximum_value

    def __repr__(self) -> str:
        boundaries = [
            repr(self.minimum_value),
            repr(self.maximum_value),
        ]

        return f"{testplates.__name__}.ranges_between({', '.join(boundaries)})"

    def __eq__(self, other: Any) -> bool:
        minimum_fits = fits_minimum_value(other, self.minimum_value)
        maximum_fits = fits_maximum_value(other, self.maximum_value)

        return minimum_fits and maximum_fits
