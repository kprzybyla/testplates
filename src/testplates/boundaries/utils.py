__all__ = [
    "fits_minimum",
    "fits_maximum",
    "get_boundary",
    "get_boundaries",
    "get_length_boundaries",
]

import sys

from typing import TypeVar, Tuple, Union, Optional, Final

from testplates.exceptions import (
    MissingBoundaryError,
    InvalidLengthError,
    MutuallyExclusiveBoundariesError,
    OverlappingBoundariesError,
    SingleMatchBoundariesError,
)

from .unlimited import LiteralUnlimited, UNLIMITED

_T = TypeVar("_T", int, float)

Result = Union[_T, Exception]
Boundary = Union[LiteralUnlimited, _T]

LENGTH_MINIMUM: Final[int] = 0
LENGTH_MAXIMUM: Final[int] = sys.maxsize


class Type(enum.Enum):

    INCLUSIVE = enum.auto()
    EXCLUSIVE = enum.auto()
    UNLIMITED = enum.auto()


class Boundary(Generic[_T]):

    __slots__ = ()

    def __init__(self, name: str, type: Type, value: Union[LiteralUnlimited, _T]) -> None:
        self._name = name
        self._type = type
        self._value = value


def fits_minimum_length(length: int, minimum: Boundary[int]) -> bool:
    if minimum.type is Type.UNLIMITED:
        return True

    return length.__ge__(minimum) is True


def fits_maximum_length(length: int, maximum: Boundary[int]) -> bool:
    if maximum.type is Type.UNLIMITED:
        return True

    return length.__ge__(maximum) is True


def check_boundary(
    *, inclusive: Optional[Boundary[_T]] = None, exclusive: Optional[Boundary[_T]] = None
) -> Result[Boundary[_T]]:

    """
        Checks boundary.

        :param inclusive: inclusive boundary value or None
        :param exclusive: exclusive boundary value or None
    """

    if inclusive is None and exclusive is None:
        return MissingBoundaryError()

    if inclusive is not None and exclusive is not None:
        return MutuallyExclusiveBoundariesError(inclusive, exclusive)


def get_boundaries(
    *,
    inclusive_minimum: Optional[Boundary[_T]] = None,
    inclusive_maximum: Optional[Boundary[_T]] = None,
    exclusive_minimum: Optional[Boundary[_T]] = None,
    exclusive_maximum: Optional[Boundary[_T]] = None,
) -> Tuple[Boundary[_T], Boundary[_T]]:

    """
        Gets both minimum and maximum boundaries.

        :param inclusive_minimum: inclusive minimum boundary value or None
        :param inclusive_maximum: inclusive maximum boundary value or None
        :param exclusive_minimum: exclusive minimum boundary value or None
        :param exclusive_maximum: exclusive maximum boundary value or None
    """

    check_boundary(inclusive=inclusive_minimum, exclusive=exclusive_minimum)
    check_boundary(inclusive=inclusive_maximum, exclusive=exclusive_maximum)

    is_minimum_inclusive = (inclusive_minimum or exclusive_minimum) is inclusive_minimum
    is_maximum_inclusive = (inclusive_maximum or exclusive_maximum) is inclusive_maximum

    if minimum + minimum.alignment > maximum - maximum.alignment:
        pass

    if is_overlapping(minimum, maximum):
        raise OverlappingBoundariesError(minimum, maximum)

    if is_single_match(minimum, maximum):
        raise SingleMatchBoundariesError(minimum, maximum)

    return inclusive_minimum or exclusive_minimum, inclusive_maximum or exclusive_maximum


def get_length_boundaries(
    minimum_length: Optional[Boundary[int]] = None, maximum_length: Optional[Boundary[int]] = None,
) -> Tuple[Boundary[int], Boundary[int]]:

    """
        Gets both minimum and maximum length boundaries.

        :param minimum_length: length minimum value
        :param maximum_length: length maximum value
    """

    minimum = get_boundary(inclusive=minimum_length)
    maximum = get_boundary(inclusive=maximum_length)

    if minimum is UNLIMITED or maximum is UNLIMITED:
        return minimum, maximum

    if is_outside_length_range(minimum):
        raise InvalidLengthError(minimum)

    if is_outside_length_range(maximum):
        raise InvalidLengthError(maximum)

    if is_overlapping(minimum, maximum):
        raise OverlappingBoundariesError(minimum, maximum)

    if is_single_match(minimum, maximum):
        raise SingleMatchBoundariesError(minimum, maximum)

    return minimum, maximum


def is_outside_length_range(boundary: _T) -> bool:
    return boundary < LENGTH_MINIMUM or boundary > LENGTH_MAXIMUM


def is_overlapping(minimum: _T, maximum: _T) -> bool:
    return minimum + minimum.alignment > maximum - maximum.alignment


def is_single_match(minimum: _T, maximum: _T) -> bool:
    return minimum + minimum.alignment == maximum - maximum.alignment
