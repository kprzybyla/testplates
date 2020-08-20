__all__ = [
    "contains",
    "has_size",
    "has_minimum_size",
    "has_maximum_size",
    "has_size_between",
    "is_one_of",
    "is_permutation_of",
    "matches_pattern",
    "ranges_between",
]

from typing import overload, AnyStr, TypeVar, List, Optional, Final

from resultful import success, failure, unwrap_success, Result

from testplates.impl.base import (
    get_minimum,
    get_maximum,
    get_value_boundaries,
    get_length_boundaries,
)

from testplates.impl.constraints import (
    Contains,
    HasLength,
    HasLengthBetween,
    IsOneOf,
    IsPermutationOf,
    RangesBetween,
    MatchesPattern,
)

from .value import Boundary, UNLIMITED
from .exceptions import TestplatesError, InsufficientValuesError, UnlimitedRangeError

_T = TypeVar("_T")

MINIMUM_NUMBER_OF_CONTAINS_VALUES: Final[int] = 1
MINIMUM_NUMBER_OF_IS_ONE_OF_VALUES: Final[int] = 2
MINIMUM_NUMBER_OF_IS_PERMUTATION_VALUES: Final[int] = 2


def contains(*values: _T) -> Result[Contains[_T], TestplatesError]:

    """
        Returns constraint object that matches any container object
        that contains all values specified via the positional arguments.

        :param values: values to be present in container object
    """

    if len(values) < MINIMUM_NUMBER_OF_CONTAINS_VALUES:
        return failure(InsufficientValuesError(MINIMUM_NUMBER_OF_CONTAINS_VALUES))

    return success(Contains(*values))


def has_size(size: int) -> Result[HasLength, TestplatesError]:

    """
        Returns constraint object that matches any sized
        object that has size equal to the exact value.

        :param size: exact size value
    """

    return success(HasLength(has_size.__name__, size))


def has_minimum_size(minimum: int, /) -> Result[HasLengthBetween, TestplatesError]:

    """
        Returns constraint object that matches any sized
        object that has size above minimum boundary value.

        :param minimum: minimum size value
    """

    result = get_minimum(inclusive=minimum)

    if not result:
        return result

    minimum_length = unwrap_success(result)

    return success(
        HasLengthBetween(
            has_minimum_size.__name__, minimum_length=minimum_length, maximum_length=UNLIMITED
        )
    )


def has_maximum_size(maximum: int, /) -> Result[HasLengthBetween, TestplatesError]:

    """
        Returns constraint object that matches any sized
        object that has size below maximum boundary value.

        :param maximum: maximum size value
    """

    result = get_maximum(inclusive=maximum)

    if not result:
        return result

    maximum_length = unwrap_success(result)

    return success(
        HasLengthBetween(
            has_maximum_size.__name__, minimum_length=UNLIMITED, maximum_length=maximum_length
        )
    )


def has_size_between(
    *, minimum: Boundary[int], maximum: Boundary[int]
) -> Result[HasLengthBetween, TestplatesError]:

    """
        Returns constraint object that matches any sized object
        that has size between minimum and maximum boundaries values.

        :param minimum: minimum size boundary value
        :param maximum: maximum size boundary value
    """

    if minimum is UNLIMITED and maximum is UNLIMITED:
        return failure(UnlimitedRangeError())

    result = get_length_boundaries(inclusive_minimum=minimum, inclusive_maximum=maximum)

    if not result:
        return result

    minimum_length, maximum_length = unwrap_success(result)

    return success(
        HasLengthBetween(
            has_size_between.__name__, minimum_length=minimum_length, maximum_length=maximum_length
        )
    )


def is_one_of(*values: _T) -> Result[IsOneOf[_T], TestplatesError]:

    """
        Returns constraint object that matches any object
        which was specified via the positional arguments.

        :param values: values to be matched by constraint object
    """

    if len(values) < MINIMUM_NUMBER_OF_IS_ONE_OF_VALUES:
        return failure(InsufficientValuesError(MINIMUM_NUMBER_OF_IS_ONE_OF_VALUES))

    return success(IsOneOf(*values))


def is_permutation_of(values: List[_T], /) -> Result[IsPermutationOf[_T], TestplatesError]:

    """
        Returns constraint object that matches any collection object
        that is a permutation of values specified via parameter.

        :param values: values to be matched as permutation
    """

    if len(values) < MINIMUM_NUMBER_OF_IS_PERMUTATION_VALUES:
        return failure(InsufficientValuesError(MINIMUM_NUMBER_OF_IS_PERMUTATION_VALUES))

    return success(IsPermutationOf(values))


def matches_pattern(pattern: AnyStr, /) -> Result[MatchesPattern[AnyStr], TestplatesError]:

    """
        Returns constraint object that matches any string
        object whose content matches the specified pattern.

        :param pattern: pattern to be matched inside string content
    """

    return success(MatchesPattern(pattern))


@overload
def ranges_between(
    *, minimum: Boundary[int], maximum: Boundary[int]
) -> Result[RangesBetween, TestplatesError]:
    ...


@overload
def ranges_between(
    *, minimum: Boundary[int], exclusive_maximum: Boundary[int]
) -> Result[RangesBetween, TestplatesError]:
    ...


@overload
def ranges_between(
    *, exclusive_minimum: Boundary[int], maximum: Boundary[int]
) -> Result[RangesBetween, TestplatesError]:
    ...


@overload
def ranges_between(
    *, exclusive_minimum: Boundary[int], exclusive_maximum: Boundary[int]
) -> Result[RangesBetween, TestplatesError]:
    ...


def ranges_between(
    *,
    minimum: Optional[Boundary[int]] = None,
    maximum: Optional[Boundary[int]] = None,
    exclusive_minimum: Optional[Boundary[int]] = None,
    exclusive_maximum: Optional[Boundary[int]] = None,
) -> Result[RangesBetween, TestplatesError]:

    """
        Returns constraint object that matches any object with boundaries
        support that ranges between minimum and maximum boundaries values.

        :param minimum: inclusive minimum boundary value
        :param maximum: inclusive maximum boundary value
        :param exclusive_minimum: exclusive minimum boundary value
        :param exclusive_maximum: exclusive maximum boundary value
    """

    if (
        (minimum is UNLIMITED and maximum is UNLIMITED)
        or (minimum is UNLIMITED and exclusive_maximum is UNLIMITED)
        or (exclusive_minimum is UNLIMITED and maximum is UNLIMITED)
        or (exclusive_minimum is UNLIMITED and exclusive_maximum is UNLIMITED)
    ):
        return failure(UnlimitedRangeError())

    result = get_value_boundaries(
        inclusive_minimum=minimum,
        inclusive_maximum=maximum,
        exclusive_minimum=exclusive_minimum,
        exclusive_maximum=exclusive_maximum,
    )

    if not result:
        return result

    minimum_value, maximum_value = unwrap_success(result)

    return success(RangesBetween(minimum_value=minimum_value, maximum_value=maximum_value))
