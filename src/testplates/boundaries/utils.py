__all__ = [
    "fits_minimum",
    "fits_maximum",
    "get_minimum",
    "get_maximum",
    "get_boundaries",
    "get_length_boundaries",
    "Boundary",
]

import sys

from typing import TypeVar, Tuple, Union, Optional, Final

from testplates.result import Result, Success, Failure
from testplates.exceptions import (
    MissingBoundaryError,
    InvalidLengthError,
    MutuallyExclusiveBoundariesError,
    OverlappingBoundariesError,
    SingleMatchBoundariesError,
)

from .limit import Extremum, Limit, MINIMUM_EXTREMUM, MAXIMUM_EXTREMUM
from .unlimited import LiteralUnlimited, UNLIMITED

_T = TypeVar("_T", int, float)

Edge = Union[LiteralUnlimited, _T]
Boundary = Union[LiteralUnlimited, Limit[_T]]

LENGTH_MINIMUM: Final[int] = 0
LENGTH_MAXIMUM: Final[int] = sys.maxsize


def get_minimum(
    inclusive: Optional[Edge[_T]] = None, exclusive: Optional[Edge[_T]] = None
) -> Result[Boundary[_T]]:

    """
        Gets minimum boundary.

        :param inclusive: inclusive boundary value or None
        :param exclusive: exclusive boundary value or None
    """

    return get_boundary(MINIMUM_EXTREMUM, inclusive=inclusive, exclusive=exclusive)


def get_maximum(
    inclusive: Optional[Edge[_T]] = None, exclusive: Optional[Edge[_T]] = None
) -> Result[Boundary[_T]]:

    """
        Gets maximum boundary.

        :param inclusive: inclusive boundary value or None
        :param exclusive: exclusive boundary value or None
    """

    return get_boundary(MAXIMUM_EXTREMUM, inclusive=inclusive, exclusive=exclusive)


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
    name: Extremum, *, inclusive: Optional[Edge[_T]] = None, exclusive: Optional[Edge[_T]] = None
) -> Result[Boundary[_T]]:

    """
        Gets boundary.

        :param name: extremum name
        :param inclusive: inclusive boundary value or None
        :param exclusive: exclusive boundary value or None
    """

    if inclusive is None and exclusive is None:
        return Failure(MissingBoundaryError(name))

    if inclusive is not None and exclusive is not None:
        return Failure(MutuallyExclusiveBoundariesError(name))

    if inclusive is not None and inclusive is not UNLIMITED:
        return Success(Limit(name, inclusive, is_inclusive=True))

    if exclusive is not None and exclusive is not UNLIMITED:
        return Success(Limit(name, exclusive, is_inclusive=False))

    return Success(UNLIMITED)


def get_boundaries(
    minimum_value: Optional[_T] = None,
    maximum_value: Optional[_T] = None,
    exclusive_minimum_value: Optional[_T] = None,
    exclusive_maximum_value: Optional[_T] = None,
) -> Result[Tuple[Boundary[_T], Boundary[_T]]]:
    minimum = get_minimum(inclusive=minimum_value, exclusive=exclusive_minimum_value)

    if minimum.is_error:
        return Failure.from_failure(minimum)

    maximum = get_maximum(inclusive=maximum_value, exclusive=exclusive_maximum_value)

    if maximum.is_error:
        return Failure.from_failure(maximum)

    outcome = check_boundaries(minimum=minimum.value, maximum=maximum.value)

    if outcome.is_error:
        return Failure.from_failure(outcome)

    return Success((minimum.value, maximum.value))


def get_length_boundaries(
    minimum_value: Optional[_T] = None,
    maximum_value: Optional[_T] = None,
    exclusive_minimum_value: Optional[_T] = None,
    exclusive_maximum_value: Optional[_T] = None,
) -> Result[Tuple[Boundary[_T], Boundary[_T]]]:
    minimum = get_minimum(inclusive=minimum_value, exclusive=exclusive_minimum_value)

    if minimum.is_error:
        return Failure.from_failure(minimum)

    maximum = get_maximum(inclusive=maximum_value, exclusive=exclusive_maximum_value)

    if maximum.is_error:
        return Failure.from_failure(maximum)

    outcome = check_length_boundaries(minimum=minimum.value, maximum=maximum.value)

    if outcome.is_error:
        return Failure.from_failure(outcome)

    return Success((minimum.value, maximum.value))


def check_boundaries(*, minimum: Boundary[_T], maximum: Boundary[_T]) -> Result[None]:

    """
        Checks minimum and maximum boundaries.

        :param minimum: minimum boundary value
        :param maximum: maximum boundary value
    """

    if minimum is UNLIMITED or maximum is UNLIMITED:
        return Success(None)

    if is_overlapping(minimum, maximum):
        return Failure(OverlappingBoundariesError(minimum, maximum))

    if is_single_match(minimum, maximum):
        return Failure(SingleMatchBoundariesError(minimum, maximum))

    return Success(None)


def check_length_boundaries(minimum: Boundary[int], maximum: Boundary[int]) -> Result[None]:

    """
        Checks minimum and maximum length boundaries.

        :param minimum: minimum length boundary value
        :param maximum: maximum length boundary value
    """

    if minimum is UNLIMITED or maximum is UNLIMITED:
        return Success(None)

    if is_outside_length_range(minimum):
        return Failure(InvalidLengthError(minimum))

    if is_outside_length_range(maximum):
        return Failure(InvalidLengthError(maximum))

    if is_overlapping(minimum, maximum):
        return Failure(OverlappingBoundariesError(minimum, maximum))

    if is_single_match(minimum, maximum):
        return Failure(SingleMatchBoundariesError(minimum, maximum))

    return Success(None)


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
