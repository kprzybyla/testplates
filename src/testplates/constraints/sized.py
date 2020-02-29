__all__ = ["has_length"]

import abc

from typing import overload, Any, Sized, Optional

from .constraint import Constraint
from .boundary import validate_boundaries


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

    __slots__ = ("_minimum", "_maximum")

    def __init__(self, *, minimum: Optional[int] = None, maximum: Optional[int] = None) -> None:
        validate_boundaries(inclusive_minimum=minimum, inclusive_maximum=maximum)

        self._minimum = minimum
        self._maximum = maximum

    def __repr__(self):
        return f"{type(self).__name__}[minimum={self._minimum}, maximum={self._maximum}]"

    def __eq__(self, other: Any) -> bool:
        if not self.is_sized(other):
            return False

        if self._minimum is not None and len(other) < self._minimum:
            return False

        if self._maximum is not None and len(other) > self._maximum:
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
        return SizedRangeTemplate(minimum=minimum, maximum=maximum)

    raise TypeError("has_length() missing 1 positional argument or 2 keyword-only arguments")
