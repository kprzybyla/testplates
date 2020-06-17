__all__ = [
    "get_minimum",
    "get_maximum",
    "fits_minimum",
    "fits_maximum",
    "check_boundaries",
    "check_length_boundaries",
    "Boundary",
]

import sys

from typing import TypeVar, Union, Optional, Final

from testplates.exceptions import (
    MissingBoundaryError,
    InvalidLengthError,
    MutuallyExclusiveBoundariesError,
    OverlappingBoundariesError,
    SingleMatchBoundariesError,
)

from .limit import Limit
from .unlimited import LiteralUnlimited, UNLIMITED

_T = TypeVar("_T", int, float)

Edge = Union[LiteralUnlimited, _T]
Boundary = Union[LiteralUnlimited, Limit[_T]]

MINIMUM_NAME: Final[str] = "minimum"
MAXIMUM_NAME: Final[str] = "maximum"

LENGTH_MINIMUM: Final[int] = 0
LENGTH_MAXIMUM: Final[int] = sys.maxsize


def get_minimum(
    inclusive: Optional[Edge[_T]] = None, exclusive: Optional[Edge[_T]] = None
) -> Union[Boundary[_T], Exception]:

    """
        Gets minimum boundary.

        :param inclusive: inclusive boundary value or None
        :param exclusive: exclusive boundary value or None
    """

    return get_boundary(MINIMUM_NAME, inclusive=inclusive, exclusive=exclusive)


def get_maximum(
    inclusive: Optional[Edge[_T]] = None, exclusive: Optional[Edge[_T]] = None
) -> Union[Boundary[_T], Exception]:

    """
        Gets maximum boundary.

        :param inclusive: inclusive boundary value or None
        :param exclusive: exclusive boundary value or None
    """

    return get_boundary(MAXIMUM_NAME, inclusive=inclusive, exclusive=exclusive)


def fits_minimum(value: _T, minimum: Boundary[_T]) -> bool:

    """
        ...

        :param value: ...
        :param minimum: ...
    """

    if minimum is UNLIMITED:
        return True

    if minimum.is_inclusive:
        return value.__ge__(minimum.value) is True
    else:
        return value.__gt__(minimum.value) is True


def fits_maximum(value: _T, maximum: Boundary[_T]) -> bool:

    """
        ...

        :param value: ...
        :param maximum: ...
    """

    if maximum is UNLIMITED:
        return True

    if maximum.is_inclusive:
        return value.__le__(maximum.value) is True
    else:
        return value.__lt__(maximum.value) is True


def get_boundary(
    name: str, *, inclusive: Optional[Edge[_T]] = None, exclusive: Optional[Edge[_T]] = None
) -> Union[Boundary[_T], Exception]:

    """
        Gets boundary.

        :param name: boundary name
        :param inclusive: inclusive boundary value or None
        :param exclusive: exclusive boundary value or None
    """

    if inclusive is None and exclusive is None:
        return MissingBoundaryError(name)

    if inclusive is not None and exclusive is not None:
        return MutuallyExclusiveBoundariesError(name)

    if inclusive is not None and inclusive is not UNLIMITED:
        return Limit(name, inclusive, is_inclusive=True)

    if exclusive is not None and exclusive is not UNLIMITED:
        return Limit(name, exclusive, is_inclusive=False)

    return UNLIMITED


def check_boundaries(*, minimum: Boundary[_T], maximum: Boundary[_T]) -> Optional[Exception]:

    """
        Checks minimum and maximum boundaries.

        :param minimum: minimum boundary value
        :param maximum: maximum boundary value
    """

    if minimum is UNLIMITED or maximum is UNLIMITED:
        return None

    if is_overlapping(minimum, maximum):
        raise OverlappingBoundariesError(minimum, maximum)

    if is_single_match(minimum, maximum):
        raise SingleMatchBoundariesError(minimum, maximum)

    return None


def check_length_boundaries(minimum: Boundary[int], maximum: Boundary[int]) -> Optional[Exception]:

    """
        Checks minimum and maximum length boundaries.

        :param minimum: minimum length boundary value
        :param maximum: maximum length boundary value
    """

    if minimum is UNLIMITED or maximum is UNLIMITED:
        return None

    if is_outside_length_range(minimum):
        raise InvalidLengthError(minimum)

    if is_outside_length_range(maximum):
        raise InvalidLengthError(maximum)

    if is_overlapping(minimum, maximum):
        raise OverlappingBoundariesError(minimum, maximum)

    if is_single_match(minimum, maximum):
        raise SingleMatchBoundariesError(minimum, maximum)

    return None


def is_outside_length_range(boundary: Limit[_T]) -> bool:

    """
        ...

        :param boundary: ...
    """

    return boundary.value < LENGTH_MINIMUM or boundary.value > LENGTH_MAXIMUM


def is_overlapping(minimum: Limit[_T], maximum: Limit[_T]) -> bool:

    """
        ...

        :param minimum: ...
        :param maximum: ...
    """

    """
        ...

        :param minimum: ...
        :param maximum: ...
    """

    return minimum.value + minimum.alignment > maximum.value - maximum.alignment


def is_single_match(minimum: Limit[_T], maximum: Limit[_T]) -> bool:

    """
        ...

        :param minimum: ...
        :param maximum: ...
    """

    return minimum.value + minimum.alignment == maximum.value - maximum.alignment
