__all__ = [
    "matches",
    "contains",
    "has_length",
    "is_one_of",
    "is_value_between",
    "is_permutation_of",
]

import re
import abc

from typing import (
    overload,
    Any,
    AnyStr,
    TypeVar,
    Generic,
    Union,
    Sized,
    Container,
    Iterable,
    Pattern,
    Optional,
)

from .abc import SupportsBoundaries
from .exceptions import MutuallyExclusiveBoundaryValueError, NotEnoughValuesError

_T = TypeVar("_T")

_Boundary = TypeVar("_Boundary", bound=SupportsBoundaries)


class Constraint(abc.ABC):

    __slots__ = ()

    @abc.abstractmethod
    def __eq__(self, other: Any) -> bool:

        """
            ...

            :param other:
        """


class OneOf(Generic[_T], Constraint):

    __slots__ = ("_values",)

    def __init__(self, *values: _T) -> None:
        if len(values) == 0:
            raise NotEnoughValuesError()

        self._values = values

    def __eq__(self, other: Any) -> bool:
        return other in self._values


class Contains(Generic[_T], Constraint):

    __slots__ = ("_values",)

    def __init__(self, *values: _T) -> None:
        if len(values) == 0:
            raise NotEnoughValuesError()

        self._values = values

    def __eq__(self, other: Any) -> bool:
        # TODO(kprzybyla): Consider throwing an exception here instead of returning False
        if not isinstance(other, Container):
            return False

        for value in self._values:
            if value not in other:
                return False

        return True


class Length(Constraint):

    __slots__ = ("_length",)

    def __init__(self, length: int) -> None:
        self._length = length

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Sized):
            return False

        return len(other) == self._length


class LengthRange(Constraint):

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
        if not isinstance(other, Sized):
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


class BetweenValue(Generic[_Boundary], Constraint):

    __slots__ = (
        "_exclusive_minimum",
        "_exclusive_maximum",
        "_inclusive_minimum",
        "_inclusive_maximum",
    )

    def __init__(
        self,
        *,
        exclusive_minimum: Optional[_Boundary] = None,
        exclusive_maximum: Optional[_Boundary] = None,
        inclusive_minimum: Optional[_Boundary] = None,
        inclusive_maximum: Optional[_Boundary] = None,
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


class AnyPattern(Generic[AnyStr], Constraint, abc.ABC):

    __slots__ = ("_pattern",)

    def __init__(self, value: AnyStr) -> None:
        self._pattern: Pattern[AnyStr] = re.compile(value)

    @abc.abstractmethod
    def has_correct_type(self, other: AnyStr) -> bool:

        """
            ...

            :param other:
        """

    def compare(self, other: AnyStr) -> bool:
        if not self.has_correct_type(other):
            return False

        return bool(self._pattern.match(other))


class StringPattern(AnyPattern[str]):

    __slots__ = ()

    def has_correct_type(self, other: AnyStr) -> bool:
        return isinstance(other, str)


class BytesPattern(AnyPattern[bytes]):

    __slots__ = ()

    def has_correct_type(self, other: AnyStr) -> bool:
        return isinstance(other, bytes)


class Permutation(Generic[_T], Constraint):

    __slots__ = ("_values",)

    def __init__(self, *values: _T) -> None:
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


def is_one_of(*values: _T) -> OneOf[_T]:
    return OneOf(*values)


def contains(*values: _T) -> Contains[_T]:
    return Contains(*values)


@overload
def has_length(length: int) -> Length:
    ...


@overload
def has_length(
    *,
    exclusive_minimum: Optional[int] = None,
    exclusive_maximum: Optional[int] = None,
    inclusive_minimum: Optional[int] = None,
    inclusive_maximum: Optional[int] = None,
) -> LengthRange:
    ...


def has_length(
    length: Optional[int] = None,
    *,
    exclusive_minimum: Optional[int] = None,
    exclusive_maximum: Optional[int] = None,
    inclusive_minimum: Optional[int] = None,
    inclusive_maximum: Optional[int] = None,
) -> Union[Length, LengthRange]:
    if length is not None:
        return Length(length)

    if (
        exclusive_minimum is not None
        or exclusive_maximum is not None
        or inclusive_minimum is not None
        or inclusive_maximum is not None
    ):
        return LengthRange(
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
            inclusive_minimum=inclusive_minimum,
            inclusive_maximum=inclusive_maximum,
        )

    raise TypeError("Function has_length() takes at least one parameter")


def is_value_between(
    *,
    exclusive_minimum: Optional[_Boundary] = None,
    exclusive_maximum: Optional[_Boundary] = None,
    inclusive_minimum: Optional[_Boundary] = None,
    inclusive_maximum: Optional[_Boundary] = None,
) -> BetweenValue[_Boundary]:
    return BetweenValue(
        exclusive_minimum=exclusive_minimum,
        exclusive_maximum=exclusive_maximum,
        inclusive_minimum=inclusive_minimum,
        inclusive_maximum=inclusive_maximum,
    )


def matches(pattern: AnyStr) -> AnyPattern[AnyStr]:
    if isinstance(pattern, str):
        return StringPattern(pattern)

    if isinstance(pattern, bytes):
        return BytesPattern(pattern)

    raise TypeError(pattern)


def is_permutation_of(*values: _T) -> Permutation[_T]:
    return Permutation(*values)
