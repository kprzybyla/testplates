from typing import overload, AnyStr, TypeVar, List, Optional

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
from .result import unwrap_success, unwrap_failure

T = TypeVar("T")


def contains(*values: T) -> Contains[T]:

    """
        Returns constraint object that matches any container object
        that contains all values specified via the positional arguments.

        :param values: values to be present in container object
    """

    return Contains(*values)


def has_length(length: int) -> HasLength:

    """
        Returns constraint object that matches any sized
        object that has length equal to the exact value.

        :param length: exact length value
    """

    return HasLength(length)


def has_length_between(
    *, minimum: Optional[Boundary[int]] = None, maximum: Optional[Boundary[int]] = None
) -> HasLengthBetween:

    """
        Returns constraint object that matches any sized object
        that has length between minimum and maximum boundaries values.

        :param minimum: minimum length boundary value
        :param maximum: maximum length boundary value
    """

    result = get_length_boundaries(inclusive_minimum=minimum, inclusive_maximum=maximum)

    if result.is_failure:
        raise unwrap_failure(result)

    minimum_boundary, maximum_boundary = unwrap_success(result)

    return HasLengthBetween(minimum=minimum_boundary, maximum=maximum_boundary)


def is_one_of(*values: T) -> IsOneOf[T]:

    """
        Returns constraint object that matches any object
        which was specified via the positional arguments.

        :param values: values to be matched by constraint object
    """

    return IsOneOf(*values)


def is_permutation_of(values: List[T], /) -> IsPermutationOf[T]:

    """
        Returns constraint object that matches any collection object
        that is a permutation of values specified via parameter.

        :param values: values to be matched as permutation
    """

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

    raise TypeError("matches() requires str or bytes as 1st argument")


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

    if result.is_failure:
        raise unwrap_failure(result)

    minimum_boundary, maximum_boundary = unwrap_success(result)

    return RangesBetween(minimum=minimum_boundary, maximum=maximum_boundary)
