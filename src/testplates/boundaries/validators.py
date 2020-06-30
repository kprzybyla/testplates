__all__ = [
    "get_value_boundaries",
    "get_length_boundaries",
    "fits_minimum",
    "fits_maximum",
    "fits_minimum_length",
    "fits_maximum_length",
    "Edge",
    "Boundary",
]

import sys

from typing import TypeVar, Sized, Tuple, Union, Optional, Final

from testplates.result import Result, Success, Failure
from testplates.exceptions import (
    MissingBoundaryError,
    InvalidLengthError,
    MutuallyExclusiveBoundariesError,
    OverlappingBoundariesError,
    SingleMatchBoundariesError,
)

from .limit import Limit, Extremum, MINIMUM_EXTREMUM, MAXIMUM_EXTREMUM
from .unlimited import LiteralUnlimited, UNLIMITED

_T = TypeVar("_T", int, float)

Edge = Union[LiteralUnlimited, _T]
Boundary = Union[LiteralUnlimited, Limit[_T]]

LENGTH_MINIMUM: Final[int] = 0
LENGTH_MAXIMUM: Final[int] = sys.maxsize

LENGTH_SPECIAL_METHOD_NAME: Final[str] = "__len__"


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


def get_value_boundaries(
    inclusive_minimum: Optional[_T] = None,
    inclusive_maximum: Optional[_T] = None,
    exclusive_minimum: Optional[_T] = None,
    exclusive_maximum: Optional[_T] = None,
) -> Result[Tuple[Boundary[_T], Boundary[_T]]]:

    """
        Gets minimum and maximum value boundaries.

        :param inclusive_minimum: inclusive minimum boundary value
        :param inclusive_maximum: inclusive maximum boundary value
        :param exclusive_minimum: exclusive minimum boundary value
        :param exclusive_maximum: exclusive maximum boundary value
    """

    if (
        inclusive_minimum is None
        and inclusive_maximum is None
        and exclusive_minimum is None
        and exclusive_maximum is None
    ):
        return Failure(TypeError("function is missing 2 required keyword-only arguments"))

    minimum = get_minimum(inclusive=inclusive_minimum, exclusive=exclusive_minimum)

    if minimum.is_error:
        return Failure.from_failure(minimum)

    maximum = get_maximum(inclusive=inclusive_maximum, exclusive=exclusive_maximum)

    if maximum.is_error:
        return Failure.from_failure(maximum)

    result = validate_value_boundaries(minimum=minimum.value, maximum=maximum.value)

    if result.is_error:
        return Failure.from_failure(result)

    return Success((minimum.value, maximum.value))


def validate_value_boundaries(*, minimum: Boundary[_T], maximum: Boundary[_T]) -> Result[None]:

    """
        Checks minimum and maximum value boundaries.

        :param minimum: minimum value boundary
        :param maximum: maximum value boundary
    """

    if minimum is UNLIMITED or maximum is UNLIMITED:
        return Success(None)

    if is_overlapping(minimum, maximum):
        return Failure(OverlappingBoundariesError(minimum, maximum))

    if is_single_match(minimum, maximum):
        return Failure(SingleMatchBoundariesError(minimum, maximum))

    return Success(None)


def get_length_boundaries(
    inclusive_minimum: Optional[_T] = None, inclusive_maximum: Optional[_T] = None
) -> Result[Tuple[Boundary[_T], Boundary[_T]]]:

    """
        Gets minimum and maximum length boundaries.

        :param inclusive_minimum: inclusive minimum boundary value
        :param inclusive_maximum: inclusive maximum boundary value
    """

    if inclusive_minimum is None and inclusive_maximum is None:
        return Failure(TypeError("function is missing 2 required keyword-only arguments"))

    minimum = get_minimum(inclusive=inclusive_minimum)

    if minimum.is_error:
        return Failure.from_failure(minimum)

    maximum = get_maximum(inclusive=inclusive_maximum)

    if maximum.is_error:
        return Failure.from_failure(maximum)

    result = validate_length_boundaries(minimum=minimum.value, maximum=maximum.value)

    if result.is_error:
        return Failure.from_failure(result)

    return Success((minimum.value, maximum.value))


def validate_length_boundaries(minimum: Boundary[int], maximum: Boundary[int]) -> Result[None]:

    """
        Checks minimum and maximum length boundaries.

        :param minimum: minimum length boundary
        :param maximum: maximum length boundary
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
        Returns True if boundary is outside of length range, otherwise False.

        :param boundary: boundary limit
    """

    return boundary.value < LENGTH_MINIMUM or boundary.value > LENGTH_MAXIMUM


def is_overlapping(minimum: Limit[_T], maximum: Limit[_T]) -> bool:

    """
        Returns True if boundaries are overlapping each other, otherwise False.

        :param minimum: minimum boundary limit
        :param maximum: maximum boundary limit
    """

    return minimum.value + minimum.alignment > maximum.value - maximum.alignment


def is_single_match(minimum: Limit[_T], maximum: Limit[_T]) -> bool:

    """
        Returns True if boundaries will match only single value, otherwise False.

        :param minimum: minimum boundary limit
        :param maximum: maximum boundary limit
    """

    return minimum.value + minimum.alignment == maximum.value - maximum.alignment


def fits_minimum(value: _T, minimum: Boundary[_T]) -> bool:

    """
        Checks whether value fits the minimum boundary.

        :param value: value to be checked against boundary
        :param minimum: minimum boundary
    """

    if minimum is UNLIMITED:
        return True

    if minimum.is_inclusive:
        return value.__ge__(minimum.value) is True
    else:
        return value.__gt__(minimum.value) is True


def fits_maximum(value: _T, maximum: Boundary[_T]) -> bool:

    """
        Checks whether value fits the maximum boundary.

        :param value: value to be checked against boundary
        :param maximum: maximum boundary
    """

    if maximum is UNLIMITED:
        return True

    if maximum.is_inclusive:
        return value.__le__(maximum.value) is True
    else:
        return value.__lt__(maximum.value) is True


def fits_minimum_length(value: Sized, minimum: Boundary[int]) -> bool:

    """
        Checks whether value size fits the minimum boundary.

        :param value: value to be checked against boundary
        :param minimum: minimum boundary
    """

    __len__ = getattr(value, LENGTH_SPECIAL_METHOD_NAME)

    if __len__ is None:
        return False

    return fits_minimum(__len__(), minimum)


def fits_maximum_length(value: Sized, maximum: Boundary[int]) -> bool:

    """
        Checks whether value size fits the maximum boundary.

        :param value: value to be checked against boundary
        :param maximum: maximum boundary
    """

    __len__ = getattr(value, LENGTH_SPECIAL_METHOD_NAME)

    if __len__ is None:
        return False

    return fits_maximum(__len__(), maximum)
