__all__ = ["has_length"]

import abc

from typing import overload, Any, Sized, Optional

from .constraint import Constraint
from .boundaries import get_minimum, get_maximum, validate_boundaries


class AnySizedTemplate(Constraint, abc.ABC):

    __slots__ = ()

    def is_sized(self, other: Any) -> bool:
        return isinstance(other, Sized)


class SizedStaticTemplate(AnySizedTemplate):

    __slots__ = ("_length",)

    def __init__(self, length: int) -> None:
        self._length = length

    def __eq__(self, other: Any) -> bool:
        if not self.is_sized(other):
            return False

        return len(other) == self._length


class SizedRangeTemplate(AnySizedTemplate):

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

        return f"{type(self).__name__}[{', '.join(parameters)}]"

    def __eq__(self, other: Any) -> bool:
        if not self.is_sized(other):
            return False

        if self._inclusive_minimum is not None and len(other) < self._inclusive_minimum:
            return False

        if self._inclusive_maximum is not None and len(other) > self._inclusive_maximum:
            return False

        return True


@overload
def has_length(length: int) -> SizedStaticTemplate:
    ...


@overload
def has_length(
    *, minimum: Optional[int] = None, maximum: Optional[int] = None
) -> SizedRangeTemplate:
    ...


def has_length(
    length: Optional[int] = None, *, minimum: Optional[int] = None, maximum: Optional[int] = None
) -> AnySizedTemplate:
    if length is not None:
        return SizedStaticTemplate(length)

    if minimum is not None or maximum is not None:
        return SizedRangeTemplate(inclusive_minimum=minimum, inclusive_maximum=maximum)

    raise TypeError("has_length() missing 1 positional argument or 2 keyword-only arguments")
