__all__ = (
    "contains",
    "has_size",
    "has_minimum_size",
    "has_maximum_size",
    "has_size_between",
    "is_one_of",
    "is_permutation_of",
    "matches_pattern",
    "ranges_between",
)

from typing import (
    overload,
    AnyStr,
    TypeVar,
    List,
    Optional,
)

# TODO(kprzybyla): Make this accessible in resultful
from resultful.impl.result import Failure

from resultful import (
    success,
    failure,
    unwrap_success,
    Result,
)

from testplates.impl.base import (
    get_minimum,
    get_maximum,
    get_value_boundaries,
    get_size_boundaries,
)

from testplates.impl.constraints import (
    Contains,
    HasSize,
    HasSizeBetween,
    IsOneOf,
    IsPermutationOf,
    RangesBetween,
    MatchesPattern,
)

from .value import (
    Boundary,
    UNLIMITED,
)

from .exceptions import (
    TestplatesError,
    UnlimitedRangeError,
)

_T = TypeVar("_T")


def contains(first: _T, /, *rest: _T) -> Result[Contains[_T], TestplatesError]:

    """
    Returns constraint object that matches any container object
    that contains all values specified via the positional arguments.

    :param first: first value to be present in the container object
    :param rest: other values to be present in container object
    """

    return success(Contains(contains.__name__, first, *rest))


def has_size(size: int) -> Result[HasSize, TestplatesError]:

    """
    Returns constraint object that matches any sized
    object that has size equal to the exact value.

    :param size: exact size value
    """

    return success(HasSize(has_size.__name__, size))


def has_minimum_size(minimum: int, /) -> Result[HasSizeBetween, TestplatesError]:

    """
    Returns constraint object that matches any sized
    object that has size above minimum boundary value.

    :param minimum: minimum size value
    """

    result = get_minimum(inclusive=minimum)

    if not result:
        return result

    minimum_size_boundary = unwrap_success(result)

    return success(
        HasSizeBetween(
            has_minimum_size.__name__,
            minimum_size=minimum_size_boundary,
            maximum_size=UNLIMITED,
        )
    )


def has_maximum_size(maximum: int, /) -> Result[HasSizeBetween, TestplatesError]:

    """
    Returns constraint object that matches any sized
    object that has size below maximum boundary value.

    :param maximum: maximum size value
    """

    result = get_maximum(inclusive=maximum)

    if not result:
        return result

    maximum_size_boundary = unwrap_success(result)

    return success(
        HasSizeBetween(
            has_maximum_size.__name__,
            minimum_size=UNLIMITED,
            maximum_size=maximum_size_boundary,
        )
    )


def has_size_between(
    *,
    minimum: Boundary[int],
    maximum: Boundary[int],
) -> Result[HasSizeBetween, TestplatesError]:

    """
    Returns constraint object that matches any sized object
    that has size between minimum and maximum boundaries values.

    :param minimum: minimum size boundary value
    :param maximum: maximum size boundary value
    """

    if minimum is UNLIMITED and maximum is UNLIMITED:
        return failure(UnlimitedRangeError())

    result = get_size_boundaries(inclusive_minimum=minimum, inclusive_maximum=maximum)

    if not result:
        return result

    minimum_size_boundary, maximum_size_boundary = unwrap_success(result)

    return success(
        HasSizeBetween(
            has_size_between.__name__,
            minimum_size=minimum_size_boundary,
            maximum_size=maximum_size_boundary,
        )
    )


def is_one_of(first: _T, second: _T, /, *rest: _T) -> Result[IsOneOf[_T], TestplatesError]:

    """
    Returns constraint object that matches any object
    which was specified via the positional arguments.

    :param first: first value to be matched by the constraint object
    :param second: second value to be matched by the constraint object
    :param rest: other values to be matched by constraint object
    """

    return success(IsOneOf(is_one_of.__name__, first, second, *rest))


def is_permutation_of(values: List[_T], /) -> Result[IsPermutationOf[_T], TestplatesError]:

    """
    Returns constraint object that matches any collection object
    that is a permutation of values specified via parameter.

    :param values: values to be matched as permutation
    """

    return success(IsPermutationOf(is_permutation_of.__name__, values))


def matches_pattern(pattern: AnyStr, /) -> Result[MatchesPattern[AnyStr], TestplatesError]:

    """
    Returns constraint object that matches any string
    object whose content matches the specified pattern.

    :param pattern: pattern to be matched inside string content
    """

    return success(MatchesPattern(matches_pattern.__name__, pattern))


@overload
def ranges_between() -> Failure[TestplatesError]:
    ...


@overload
def ranges_between(
    *,
    minimum: Boundary[int],
) -> Failure[TestplatesError]:
    ...


@overload
def ranges_between(
    *,
    maximum: Boundary[int],
) -> Failure[TestplatesError]:
    ...


@overload
def ranges_between(
    *,
    exclusive_minimum: Boundary[int],
) -> Failure[TestplatesError]:
    ...


@overload
def ranges_between(
    *,
    exclusive_maximum: Boundary[int],
) -> Failure[TestplatesError]:
    ...


@overload
def ranges_between(
    *,
    minimum: Boundary[int],
    maximum: Boundary[int],
    exclusive_minimum: Boundary[int],
) -> Failure[TestplatesError]:
    ...


@overload
def ranges_between(
    *,
    minimum: Boundary[int],
    maximum: Boundary[int],
    exclusive_maximum: Boundary[int],
) -> Failure[TestplatesError]:
    ...


@overload
def ranges_between(
    *,
    minimum: Boundary[int],
    exclusive_minimum: Boundary[int],
    exclusive_maximum: Boundary[int],
) -> Failure[TestplatesError]:
    ...


@overload
def ranges_between(
    *,
    maximum: Boundary[int],
    exclusive_minimum: Boundary[int],
    exclusive_maximum: Boundary[int],
) -> Failure[TestplatesError]:
    ...


@overload
def ranges_between(
    *,
    minimum: Boundary[int],
    maximum: Boundary[int],
    exclusive_minimum: Boundary[int],
    exclusive_maximum: Boundary[int],
) -> Failure[TestplatesError]:
    ...


@overload
def ranges_between(
    *,
    minimum: Boundary[int],
    maximum: Boundary[int],
) -> Result[RangesBetween, TestplatesError]:
    ...


@overload
def ranges_between(
    *,
    minimum: Boundary[int],
    exclusive_maximum: Boundary[int],
) -> Result[RangesBetween, TestplatesError]:
    ...


@overload
def ranges_between(
    *,
    exclusive_minimum: Boundary[int],
    maximum: Boundary[int],
) -> Result[RangesBetween, TestplatesError]:
    ...


@overload
def ranges_between(
    *,
    exclusive_minimum: Boundary[int],
    exclusive_maximum: Boundary[int],
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

    minimum_value_boundary, maximum_value_boundary = unwrap_success(result)

    return success(
        RangesBetween(
            ranges_between.__name__,
            minimum_value=minimum_value_boundary,
            maximum_value=maximum_value_boundary,
        )
    )
