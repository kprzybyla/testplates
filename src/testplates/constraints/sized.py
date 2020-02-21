__all__ = ["has_length"]

import abc

from typing import overload, Any, Sized, Optional

from testplates.exceptions import MutuallyExclusiveBoundaryValueError

from .constraint import Constraint


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

    __slots__ = (
        "_exclusive_minimum",
        "_exclusive_maximum",
        "_inclusive_minimum",
        "_inclusive_maximum",
    )

    def __init__(
        self,
        *,
        exclusive_minimum: Optional[int] = None,
        exclusive_maximum: Optional[int] = None,
        inclusive_minimum: Optional[int] = None,
        inclusive_maximum: Optional[int] = None,
    ) -> None:
        self._exclusive_minimum = exclusive_minimum
        self._exclusive_maximum = exclusive_maximum
        self._inclusive_minimum = inclusive_minimum
        self._inclusive_maximum = inclusive_maximum

        if self._exclusive_minimum is not None and self._inclusive_minimum is not None:
            raise MutuallyExclusiveBoundaryValueError()

        if self._exclusive_maximum is not None and self._inclusive_maximum is not None:
            raise MutuallyExclusiveBoundaryValueError()

    def __eq__(self, other: Any) -> bool:
        if not self.is_sized(other):
            return False

        if self._exclusive_minimum is not None and len(other) <= self._exclusive_minimum:
            return False

        if self._exclusive_maximum is not None and len(other) >= self._exclusive_maximum:
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
    *,
    exclusive_minimum: Optional[int] = None,
    exclusive_maximum: Optional[int] = None,
    inclusive_minimum: Optional[int] = None,
    inclusive_maximum: Optional[int] = None,
) -> SizedRangeTemplate:
    ...


def has_length(
    length: Optional[int] = None,
    *,
    exclusive_minimum: Optional[int] = None,
    exclusive_maximum: Optional[int] = None,
    inclusive_minimum: Optional[int] = None,
    inclusive_maximum: Optional[int] = None,
) -> AnySizedTemplate:
    if length is not None:
        return SizedStaticTemplate(length)

    if (
        exclusive_minimum is not None
        or exclusive_maximum is not None
        or inclusive_minimum is not None
        or inclusive_maximum is not None
    ):
        return SizedRangeTemplate(
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
            inclusive_minimum=inclusive_minimum,
            inclusive_maximum=inclusive_maximum,
        )

    raise TypeError("has_length() takes at least 1 positional argument or 4 keyword arguments")
