__all__ = [
    "OneOf",
    "Contains",
    "Length",
    "BetweenLength",
    "BetweenValue",
    "MatchesString",
    "MatchesBytes",
    "Permutation",
]

import re
import abc

from typing import Any, AnyStr, TypeVar, Generic, Sized, Container, Iterable, Pattern, Optional

from .abc import SupportsBoundaries
from .exceptions import ExclusiveInclusiveValueError

T = TypeVar("T")
Boundary = TypeVar("Boundary", bound=SupportsBoundaries)


class OneOf(Generic[T]):

    __slots__ = ("_values",)

    def __init__(self, *values: T) -> None:
        self._values = values

    def __eq__(self, other: Any) -> bool:
        return other in self._values


class Contains(Generic[T]):

    __slots__ = ("_values",)

    def __init__(self, *values: T) -> None:
        self._values = values

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Container):
            return False

        for value in self._values:
            if value not in other:
                return False

        return True


class Length:

    __slots__ = ("_length",)

    def __init__(self, length: int) -> None:
        self._length = length

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Sized):
            return False

        return len(other) == self._length


class BetweenLength(Generic[Boundary]):

    __slots__ = ("_minimum", "_maximum")

    def __init__(
        self, *, minimum: Optional[Boundary] = None, maximum: Optional[Boundary] = None
    ) -> None:
        self._minimum = minimum
        self._maximum = maximum

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Sized):
            return False

        if self._minimum is not None and len(other) < self._minimum:
            return False

        if self._maximum is not None and len(other) > self._maximum:
            return False

        return True


class BetweenValue(Generic[Boundary]):

    __slots__ = (
        "_exclusive_minimum",
        "_exclusive_maximum",
        "_inclusive_minimum",
        "_inclusive_maximum",
    )

    def __init__(
        self,
        *,
        exclusive_minimum: Optional[Boundary] = None,
        exclusive_maximum: Optional[Boundary] = None,
        inclusive_minimum: Optional[Boundary] = None,
        inclusive_maximum: Optional[Boundary] = None,
    ) -> None:
        self._exclusive_minimum = exclusive_minimum
        self._exclusive_maximum = exclusive_maximum
        self._inclusive_minimum = inclusive_minimum
        self._inclusive_maximum = inclusive_maximum

        if self._exclusive_minimum is not None and self._inclusive_minimum is not None:
            raise ExclusiveInclusiveValueError(self._exclusive_minimum, self._inclusive_minimum)

        if self._exclusive_maximum is not None and self._inclusive_maximum is not None:
            raise ExclusiveInclusiveValueError(self._exclusive_maximum, self._inclusive_maximum)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, SupportsBoundaries):
            return False

        if self._exclusive_minimum is not None and other < self._exclusive_minimum:
            return False

        if self._exclusive_maximum is not None and other > self._exclusive_maximum:
            return False

        if self._inclusive_minimum is not None and other <= self._inclusive_minimum:
            return False

        if self._inclusive_maximum is not None and other >= self._inclusive_maximum:
            return False

        return True


class Matches(Generic[AnyStr], abc.ABC):

    __slots__ = ("_pattern",)

    def __init__(self, value: AnyStr) -> None:
        self._pattern: Pattern[AnyStr] = re.compile(value)

    @abc.abstractmethod
    def __eq__(self, other: Any) -> bool:
        ...

    def compare(self, other: AnyStr) -> bool:
        return bool(self._pattern.match(other))


class MatchesString(Matches[str]):

    __slots__ = ()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, str):
            return False

        return self.compare(other)


class MatchesBytes(Matches[bytes]):

    __slots__ = ()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, bytes):
            return False

        return self.compare(other)


class Permutation(Generic[T]):

    __slots__ = ("_values",)

    def __init__(self, *values: T) -> None:
        self._values = values

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Iterable):
            return False

        values = list(self._values)

        for value in other:
            try:
                found = values.index(value)
            except IndexError:
                return False
            else:
                values.pop(found)

        return len(values) == 0
