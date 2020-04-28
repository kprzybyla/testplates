__all__ = [
    "get_minimum",
    "get_maximum",
    "get_boundaries",
    "get_length_boundaries",
    "Inclusive",
    "Exclusive",
]

import sys

from typing import TypeVar, Tuple, Optional, Final

from testplates.abc import Boundary
from testplates.exceptions import (
    InvalidLengthError,
    MutuallyExclusiveBoundariesError,
    OverlappingBoundariesError,
    SingleMatchBoundariesError,
)

_T = TypeVar("_T", int, float)

MINIMUM_NAME: Final[str] = "minimum"
MAXIMUM_NAME: Final[str] = "maximum"

INCLUSIVE_NAME: Final[str] = "inclusive"
EXCLUSIVE_NAME: Final[str] = "exclusive"
UNLIMITED_NAME: Final[str] = "unlimited"

INCLUSIVE_ALIGNMENT: Final[int] = 0
EXCLUSIVE_ALIGNMENT: Final[int] = 1

LENGTH_MINIMUM: Final[int] = 0
LENGTH_MAXIMUM: Final[int] = sys.maxsize


class Inclusive(Boundary[_T]):

    __slots__ = ()

    def __repr__(self) -> str:
        return f"{self.name}={self.value}"

    @property
    def type(self) -> str:
        return INCLUSIVE_NAME

    @property
    def alignment(self) -> int:
        return INCLUSIVE_ALIGNMENT

    def fits(self, value: _T, /) -> bool:
        if self.name == MINIMUM_NAME and value.__ge__(self.value) is not True:
            return False

        if self.name == MAXIMUM_NAME and value.__le__(self.value) is not True:
            return False

        return True


class Exclusive(Boundary[_T]):

    __slots__ = ()

    def __repr__(self) -> str:
        return f"{self.type}_{self.name}={self.value}"

    @property
    def type(self) -> str:
        return EXCLUSIVE_NAME

    @property
    def alignment(self) -> int:
        return EXCLUSIVE_ALIGNMENT

    def fits(self, value: _T, /) -> bool:
        if self.name == MINIMUM_NAME and value.__gt__(self.value) is not True:
            return False

        if self.name == MAXIMUM_NAME and value.__lt__(self.value) is not True:
            return False

        return True


class Unlimited(Boundary[_T]):

    __slots__ = ()

    @property
    def type(self) -> str:
        return UNLIMITED_NAME

    @property
    def alignment(self) -> int:
        raise NotImplementedError()

    def fits(self, value: _T, /) -> bool:
        return True


def get_minimum(*, inclusive: Optional[_T] = None, exclusive: Optional[_T] = None) -> Boundary[_T]:

    """
        Gets minimum boundary.

        :param inclusive: inclusive boundary value or None
        :param exclusive: exclusive boundary value or None
    """

    return _get_boundary(MINIMUM_NAME, inclusive=inclusive, exclusive=exclusive)


def get_maximum(*, inclusive: Optional[_T] = None, exclusive: Optional[_T] = None) -> Boundary[_T]:

    """
        Gets maximum boundary.

        :param inclusive: inclusive boundary value or None
        :param exclusive: exclusive boundary value or None
    """

    return _get_boundary(MAXIMUM_NAME, inclusive=inclusive, exclusive=exclusive)


def get_boundaries(
    *,
    inclusive_minimum: Optional[_T] = None,
    inclusive_maximum: Optional[_T] = None,
    exclusive_minimum: Optional[_T] = None,
    exclusive_maximum: Optional[_T] = None,
) -> Tuple[Boundary[_T], Boundary[_T]]:

    """
        Gets both minimum and maximum boundaries.

        :param inclusive_minimum: inclusive minimum boundary value or None
        :param inclusive_maximum: inclusive maximum boundary value or None
        :param exclusive_minimum: exclusive minimum boundary value or None
        :param exclusive_maximum: exclusive maximum boundary value or None
    """

    minimum = get_minimum(inclusive=inclusive_minimum, exclusive=exclusive_minimum)
    maximum = get_maximum(inclusive=inclusive_maximum, exclusive=exclusive_maximum)

    if isinstance(minimum, Unlimited) or isinstance(maximum, Unlimited):
        return minimum, maximum

    if minimum.value + minimum.alignment > maximum.value - maximum.alignment:
        raise OverlappingBoundariesError(minimum, maximum)

    if minimum.value + minimum.alignment == maximum.value - maximum.alignment:
        raise SingleMatchBoundariesError(minimum, maximum)

    return minimum, maximum


def get_length_boundaries(
    *, inclusive_minimum: Optional[int] = None, inclusive_maximum: Optional[int] = None
) -> Tuple[Boundary[int], Boundary[int]]:

    """
        Gets both minimum and maximum length boundaries.

        :param inclusive_minimum: length minimum value
        :param inclusive_maximum: length maximum value
    """

    minimum = get_minimum(inclusive=inclusive_minimum)
    maximum = get_maximum(inclusive=inclusive_maximum)

    if minimum.value < LENGTH_MINIMUM or minimum.value > LENGTH_MAXIMUM:
        raise InvalidLengthError(minimum)

    if maximum.value < LENGTH_MINIMUM or maximum.value > LENGTH_MAXIMUM:
        raise InvalidLengthError(maximum)

    if minimum.value + minimum.alignment > maximum.value - maximum.alignment:
        raise OverlappingBoundariesError(minimum, maximum)

    if minimum.value + minimum.alignment == maximum.value - maximum.alignment:
        raise SingleMatchBoundariesError(minimum, maximum)

    return minimum, maximum


def _get_boundary(
    name: str, /, *, inclusive: Optional[_T] = None, exclusive: Optional[_T] = None
) -> Boundary[_T]:

    """
        Gets either inclusive or exclusive
        boundary with given name and value.

        :param name: boundary name
        :param inclusive: inclusive boundary value
        :param exclusive: exclusive boundary value
    """

    if inclusive is not None and exclusive is not None:
        raise MutuallyExclusiveBoundariesError(name)

    if inclusive is not None:
        return Inclusive(name, inclusive)

    if exclusive is not None:
        return Exclusive(name, exclusive)

    return Unlimited(name, None)
