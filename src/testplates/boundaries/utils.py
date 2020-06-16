__all__ = [
    "get_minimum",
    "get_maximum",
    "get_boundaries",
    "get_length_boundaries",
]

import sys

from typing import TypeVar, Tuple, Union, Optional, Final

from testplates.abc import Boundary, LiteralBoundary
from testplates.exceptions import (
    MissingBoundaryError,
    InvalidLengthError,
    MutuallyExclusiveBoundariesError,
    OverlappingBoundariesError,
    SingleMatchBoundariesError,
)

from .unlimited import LiteralUnlimited, UNLIMITED
from .boundaries import (
    Unlimited,
    InclusiveMinimum,
    InclusiveMaximum,
    ExclusiveMinimum,
    ExclusiveMaximum,
)

_T = TypeVar("_T", int, float)

BoundaryValue = Union[LiteralUnlimited, _T]

LENGTH_MINIMUM: Final[int] = 0
LENGTH_MAXIMUM: Final[int] = sys.maxsize


def get_minimum(
    *,
    inclusive: Optional[BoundaryValue[_T]] = None,
    exclusive: Optional[BoundaryValue[_T]] = None,
) -> Boundary[_T]:

    """
        Gets minimum boundary.

        :param inclusive: inclusive boundary value or None
        :param exclusive: exclusive boundary value or None
    """

    if inclusive is not None and exclusive is not None:
        raise MutuallyExclusiveBoundariesError(inclusive, exclusive)

    if (inclusive or exclusive) is UNLIMITED:
        return Unlimited()

    if inclusive is not None:
        return InclusiveMinimum(inclusive)

    if exclusive is not None:
        return ExclusiveMinimum(exclusive)

    raise MissingBoundaryError()


def get_maximum(
    *,
    inclusive: Optional[BoundaryValue[_T]] = None,
    exclusive: Optional[BoundaryValue[_T]] = None,
) -> Boundary[_T]:

    """
        Gets maximum boundary.

        :param inclusive: inclusive boundary value or None
        :param exclusive: exclusive boundary value or None
    """

    if inclusive is not None and exclusive is not None:
        raise MutuallyExclusiveBoundariesError(inclusive, exclusive)

    if (inclusive or exclusive) is UNLIMITED:
        return Unlimited()

    if inclusive is not None:
        return InclusiveMaximum(inclusive)

    if exclusive is not None:
        return ExclusiveMaximum(exclusive)

    raise MissingBoundaryError()


def get_boundaries(
    *,
    inclusive_minimum: Optional[BoundaryValue[_T]] = None,
    inclusive_maximum: Optional[BoundaryValue[_T]] = None,
    exclusive_minimum: Optional[BoundaryValue[_T]] = None,
    exclusive_maximum: Optional[BoundaryValue[_T]] = None,
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

    if is_unlimited(minimum) or is_unlimited(maximum):
        return minimum, maximum

    assert isinstance(minimum, LiteralBoundary)
    assert isinstance(maximum, LiteralBoundary)

    if is_overlapping(minimum, maximum):
        raise OverlappingBoundariesError(minimum, maximum)

    if is_single_match(minimum, maximum):
        raise SingleMatchBoundariesError(minimum, maximum)

    return minimum, maximum


def get_length_boundaries(
    minimum_length: Optional[BoundaryValue[int]] = None,
    maximum_length: Optional[BoundaryValue[int]] = None,
) -> Tuple[Boundary[int], Boundary[int]]:

    """
        Gets both minimum and maximum length boundaries.

        :param minimum_length: length minimum value
        :param maximum_length: length maximum value
    """

    minimum = get_minimum(inclusive=minimum_length)
    maximum = get_maximum(inclusive=maximum_length)

    if is_unlimited(minimum) or is_unlimited(maximum):
        return minimum, maximum

    assert isinstance(minimum, LiteralBoundary)
    assert isinstance(maximum, LiteralBoundary)

    if is_outside_length_range(minimum):
        raise InvalidLengthError(minimum)

    if is_outside_length_range(maximum):
        raise InvalidLengthError(maximum)

    if is_overlapping(minimum, maximum):
        raise OverlappingBoundariesError(minimum, maximum)

    if is_single_match(minimum, maximum):
        raise SingleMatchBoundariesError(minimum, maximum)

    return minimum, maximum


def is_unlimited(boundary: Boundary[_T]) -> bool:
    return isinstance(boundary, Unlimited)


def is_outside_length_range(boundary: LiteralBoundary[_T]) -> bool:
    return boundary.value < LENGTH_MINIMUM or boundary.value > LENGTH_MAXIMUM


def is_overlapping(minimum: LiteralBoundary[_T], maximum: LiteralBoundary[_T]) -> bool:
    return minimum.value + minimum.alignment > maximum.value - maximum.alignment


def is_single_match(minimum: LiteralBoundary[_T], maximum: LiteralBoundary[_T]) -> bool:
    return minimum.value + minimum.alignment == maximum.value - maximum.alignment
