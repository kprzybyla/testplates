__all__ = [
    "contains",
    "has_size",
    "has_size_between",
    "is_one_of",
    "is_permutation_of",
    "matches_pattern",
    "ranges_between",
]

from typing import overload, AnyStr, TypeVar, List, Optional, Final

from resultful import unwrap_success, unwrap_failure

from testplates.impl.base import get_value_boundaries, get_length_boundaries
from testplates.impl.constraints import (
    Contains,
    HasLength,
    HasLengthBetween,
    IsOneOf,
    IsPermutationOf,
    RangesBetween,
    MatchesPattern,
)

from .value import Boundary
from .exceptions import InvalidSignatureError, InsufficientValuesError

_T = TypeVar("_T")

MINIMUM_NUMBER_OF_CONTAINS_VALUES: Final[int] = 1
MINIMUM_NUMBER_OF_IS_ONE_OF_VALUES: Final[int] = 2
MINIMUM_NUMBER_OF_IS_PERMUTATION_VALUES: Final[int] = 2


def contains(*values: _T) -> Contains[_T]:

    """
        Returns constraint object that matches any container object
        that contains all values specified via the positional arguments.

        :param values: values to be present in container object
    """

    if len(values) < MINIMUM_NUMBER_OF_CONTAINS_VALUES:
        raise InsufficientValuesError(MINIMUM_NUMBER_OF_CONTAINS_VALUES)

    return Contains(*values)


def has_size(size: int) -> HasLength:

    """
        Returns constraint object that matches any sized
        object that has size equal to the exact value.

        :param size: exact size value
    """

    return HasLength(size)


def has_size_between(
    *, minimum: Optional[Boundary[int]] = None, maximum: Optional[Boundary[int]] = None
) -> HasLengthBetween:

    """
        Returns constraint object that matches any sized object
        that has size between minimum and maximum boundaries values.

        :param minimum: minimum size boundary value
        :param maximum: maximum size boundary value
    """

    result = get_length_boundaries(inclusive_minimum=minimum, inclusive_maximum=maximum)

    if not result:
        raise unwrap_failure(result)

    minimum_length, maximum_length = unwrap_success(result)

    return HasLengthBetween(minimum_length=minimum_length, maximum_length=maximum_length)


def is_one_of(*values: _T) -> IsOneOf[_T]:

    """
        Returns constraint object that matches any object
        which was specified via the positional arguments.

        :param values: values to be matched by constraint object
    """

    if len(values) < MINIMUM_NUMBER_OF_IS_ONE_OF_VALUES:
        raise InsufficientValuesError(MINIMUM_NUMBER_OF_IS_ONE_OF_VALUES)

    return IsOneOf(*values)


def is_permutation_of(values: List[_T], /) -> IsPermutationOf[_T]:

    """
        Returns constraint object that matches any collection object
        that is a permutation of values specified via parameter.

        :param values: values to be matched as permutation
    """

    if len(values) < MINIMUM_NUMBER_OF_IS_PERMUTATION_VALUES:
        raise InsufficientValuesError(MINIMUM_NUMBER_OF_IS_PERMUTATION_VALUES)

    return IsPermutationOf(values)


def matches_pattern(pattern: AnyStr, /) -> MatchesPattern[AnyStr]:

    """
        Returns constraint object that matches any string
        object whose content matches the specified pattern.

        :param pattern: pattern to be matched inside string content
    """

    if isinstance(pattern, str):
        return MatchesPattern(pattern, str)

    if isinstance(pattern, bytes):
        return MatchesPattern(pattern, bytes)

    raise InvalidSignatureError("matches() requires str or bytes as 1st argument")


@overload
def ranges_between(
    *, minimum: Optional[Boundary[int]], maximum: Optional[Boundary[int]]
) -> RangesBetween:
    ...


@overload
def ranges_between(
    *, minimum: Optional[Boundary[int]], exclusive_maximum: Optional[Boundary[int]]
) -> RangesBetween:
    ...


@overload
def ranges_between(
    *, exclusive_minimum: Optional[Boundary[int]], maximum: Optional[Boundary[int]]
) -> RangesBetween:
    ...


@overload
def ranges_between(
    *, exclusive_minimum: Optional[Boundary[int]], exclusive_maximum: Optional[Boundary[int]]
) -> RangesBetween:
    ...


def ranges_between(
    *,
    minimum: Optional[Boundary[int]] = None,
    maximum: Optional[Boundary[int]] = None,
    exclusive_minimum: Optional[Boundary[int]] = None,
    exclusive_maximum: Optional[Boundary[int]] = None,
) -> RangesBetween:

    """
        Returns constraint object that matches any object with boundaries
        support that ranges between minimum and maximum boundaries values.

        :param minimum: inclusive minimum boundary value
        :param maximum: inclusive maximum boundary value
        :param exclusive_minimum: exclusive minimum boundary value
        :param exclusive_maximum: exclusive maximum boundary value
    """

    result = get_value_boundaries(
        inclusive_minimum=minimum,
        inclusive_maximum=maximum,
        exclusive_minimum=exclusive_minimum,
        exclusive_maximum=exclusive_maximum,
    )

    if not result:
        raise unwrap_failure(result)

    minimum_value, maximum_value = unwrap_success(result)

    return RangesBetween(minimum_value=minimum_value, maximum_value=maximum_value)
