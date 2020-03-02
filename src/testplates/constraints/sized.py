__all__ = ["has_length"]

import abc

from typing import overload, Any, Sized, Optional

from testplates import __module__
from testplates.abc import Constraint

from .boundaries import get_minimum, get_maximum, validate_boundaries


class AnyHasLength(Constraint, abc.ABC):

    __slots__ = ()

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Sized)


class HasLength(AnyHasLength):

    __slots__ = ("_length",)

    def __init__(self, length: int) -> None:
        self._length = length

    def __repr__(self) -> str:
        return f"{__module__}.{type(self).__name__}[{self._length}]"

    def __eq__(self, other: Any) -> bool:
        if not super().__eq__(other):
            return False

        return len(other) == self._length


class HasLengthBetween(AnyHasLength):

    __slots__ = ("_inclusive_minimum", "_inclusive_maximum")

    def __init__(
        self, *, inclusive_minimum: Optional[int] = None, inclusive_maximum: Optional[int] = None
    ) -> None:
        validate_boundaries(
            inclusive_minimum=inclusive_minimum, inclusive_maximum=inclusive_maximum
        )

        self._inclusive_minimum = inclusive_minimum
        self._inclusive_maximum = inclusive_maximum

    def __repr__(self):
        minimum = get_minimum(inclusive=self._inclusive_minimum)
        maximum = get_maximum(inclusive=self._inclusive_maximum)

        parameters = [
            f"{minimum.type}_{minimum.name}={minimum.value}",
            f"{maximum.type}_{maximum.name}={maximum.value}",
        ]

        return f"{__module__}.{type(self).__name__}[{', '.join(parameters)}]"

    def __eq__(self, other: Any) -> bool:
        if not super().__eq__(other):
            return False

        if self._inclusive_minimum is not None and len(other) < self._inclusive_minimum:
            return False

        if self._inclusive_maximum is not None and len(other) > self._inclusive_maximum:
            return False

        return True


@overload
def has_length(length: int) -> HasLength:
    ...


@overload
def has_length(
    *, minimum: Optional[int] = None, maximum: Optional[int] = None
) -> HasLengthBetween:
    ...


def has_length(
    length: Optional[int] = None, *, minimum: Optional[int] = None, maximum: Optional[int] = None
) -> AnyHasLength:
    if length is not None:
        return HasLength(length)

    if minimum is not None or maximum is not None:
        return HasLengthBetween(inclusive_minimum=minimum, inclusive_maximum=maximum)

    raise TypeError("has_length() missing 1 positional argument or 2 keyword-only arguments")
