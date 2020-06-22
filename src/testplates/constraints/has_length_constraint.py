__all__ = ["has_length"]

import abc

from typing import overload, Any, Sized, Optional

import testplates

from testplates.abc import Constraint
from testplates.boundaries import get_length_boundaries, fits_minimum, fits_maximum


class AnyHasLength(Constraint, abc.ABC):

    __slots__ = ()

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Sized)


class HasLength(AnyHasLength):

    __slots__ = ("_length",)

    def __init__(self, length: int, /) -> None:
        self._length = length

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{has_length.__name__}({self._length})"

    def __eq__(self, other: Any) -> bool:
        if not super().__eq__(other):
            return False

        return len(other) == self._length


class HasLengthBetween(AnyHasLength):

    __slots__ = ("_minimum", "_maximum")

    def __init__(
        self, *, minimum_length: Optional[int] = None, maximum_length: Optional[int] = None
    ) -> None:
        result = get_length_boundaries(
            inclusive_minimum=minimum_length, inclusive_maximum=maximum_length
        )

        if result.is_error:
            raise result.error

        self._minimum, self._maximum = result.value

    def __repr__(self) -> str:
        boundaries = [
            repr(self._minimum),
            repr(self._maximum),
        ]

        return f"{testplates.__name__}.{has_length.__name__}({', '.join(boundaries)})"

    def __eq__(self, other: Any) -> bool:
        if not super().__eq__(other):
            return False

        length = len(other)

        minimum_fits = fits_minimum(length, self._minimum)
        maximum_fits = fits_maximum(length, self._maximum)

        return minimum_fits and maximum_fits


@overload
def has_length(length: int, /) -> HasLength:
    ...


@overload
def has_length(*, minimum: int, maximum: int) -> HasLengthBetween:
    ...


def has_length(
    length: Optional[int] = None,
    /,
    *,
    minimum: Optional[int] = None,
    maximum: Optional[int] = None,
) -> AnyHasLength:

    """
        Returns constraint object that matches any sized object
        that has length equal to the exact value or length
        between minimum and maximum boundaries values.

        :param length: exact length value
        :param minimum: minimum length boundary value
        :param maximum: maximum length boundary value
    """

    if length is not None:
        return HasLength(length)

    if minimum is not None or maximum is not None:
        return HasLengthBetween(minimum_length=minimum, maximum_length=maximum)

    raise TypeError("function is missing 1 positional argument or 2 keyword-only arguments")
