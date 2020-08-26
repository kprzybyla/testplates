from typing import Any, Optional, Literal, Final

from resultful import (
    unwrap_success,
    unwrap_failure,
)

from hypothesis import (
    assume,
    given,
    strategies as st,
)

from testplates import (
    ranges_between,
    UNLIMITED,
    MissingBoundaryError,
    UnlimitedRangeError,
    MutuallyExclusiveBoundariesError,
    OverlappingBoundariesError,
    SingleMatchBoundariesError,
)

from tests.strategies import Draw

MINIMUM_EXTREMUM: Final[Literal["minimum"]] = "minimum"
MAXIMUM_EXTREMUM: Final[Literal["maximum"]] = "maximum"

EXCLUSIVE_ALIGNMENT: Final[int] = 1


class NotComparable:

    __slots__ = ()

    def __gt__(self, other: Any) -> bool:
        return NotImplemented

    def __lt__(self, other: Any) -> bool:
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        return NotImplemented


@st.composite
def st_value(
    draw: Draw[int],
    min_value: Optional[int] = None,
    max_value: Optional[int] = None,
) -> int:
    return draw(st.integers(min_value=min_value, max_value=max_value))  # type: ignore


@st.composite
def st_inclusive_minimum(draw: Draw[int], value: int) -> int:
    return draw(st.integers(max_value=value))


@st.composite
def st_inclusive_maximum(draw: Draw[int], value: int) -> int:
    return draw(st.integers(min_value=value))


@st.composite
def st_exclusive_minimum(draw: Draw[int], value: int) -> int:
    minimum = draw(st_inclusive_minimum(value))
    assume(value != minimum)

    return minimum


@st.composite
def st_exclusive_maximum(draw: Draw[int], value: int) -> int:
    maximum = draw(st_inclusive_maximum(value))
    assume(value != maximum)

    return maximum


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_repr_with_inclusive_minimum_and_inclusive_maximum(
    data: st.DataObject,
    value: int,
) -> None:
    fmt = "testplates.ranges_between(minimum={minimum}, maximum={maximum})"

    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    assume(inclusive_minimum != inclusive_maximum)

    assert (result := ranges_between(minimum=inclusive_minimum, maximum=inclusive_maximum))

    constraint = unwrap_success(result)
    assert repr(constraint) == fmt.format(minimum=inclusive_minimum, maximum=inclusive_maximum)


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_repr_with_inclusive_minimum_and_exclusive_maximum(
    data: st.DataObject,
    value: int,
) -> None:
    fmt = "testplates.ranges_between(minimum={minimum}, exclusive_maximum={maximum})"

    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    assume(inclusive_minimum != exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    assert (
        result := ranges_between(
            minimum=inclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    constraint = unwrap_success(result)
    assert repr(constraint) == fmt.format(minimum=inclusive_minimum, maximum=exclusive_maximum)


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_repr_with_exclusive_minimum_and_inclusive_maximum(
    data: st.DataObject,
    value: int,
) -> None:
    fmt = "testplates.ranges_between(exclusive_minimum={minimum}, maximum={maximum})"

    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT != inclusive_maximum)

    assert (
        result := ranges_between(
            exclusive_minimum=exclusive_minimum,
            maximum=inclusive_maximum,
        )
    )

    constraint = unwrap_success(result)
    assert repr(constraint) == fmt.format(minimum=exclusive_minimum, maximum=inclusive_maximum)


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_repr_with_exclusive_minimum_and_exclusive_maximum(
    data: st.DataObject,
    value: int,
) -> None:
    fmt = "testplates.ranges_between(exclusive_minimum={minimum}, exclusive_maximum={maximum})"

    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT != exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    assert (
        result := ranges_between(
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    constraint = unwrap_success(result)
    assert repr(constraint) == fmt.format(minimum=exclusive_minimum, maximum=exclusive_maximum)


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_success_with_inclusive_minimum_and_inclusive_maximum(
    data: st.DataObject,
    value: int,
) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    assume(inclusive_minimum != inclusive_maximum)

    assert (result := ranges_between(minimum=inclusive_minimum, maximum=inclusive_maximum))

    constraint = unwrap_success(result)
    assert constraint == value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_success_with_inclusive_minimum_and_exclusive_maximum(
    data: st.DataObject,
    value: int,
) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    assume(inclusive_minimum != exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    assert (
        result := ranges_between(
            minimum=inclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    constraint = unwrap_success(result)
    assert constraint == value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_success_with_exclusive_minimum_and_inclusive_maximum(
    data: st.DataObject,
    value: int,
) -> None:
    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT != inclusive_maximum)

    assert (
        result := ranges_between(
            exclusive_minimum=exclusive_minimum,
            maximum=inclusive_maximum,
        )
    )

    constraint = unwrap_success(result)
    assert constraint == value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_success_with_exclusive_minimum_and_exclusive_maximum(
    data: st.DataObject,
    value: int,
) -> None:
    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT != exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    assert (
        result := ranges_between(
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    constraint = unwrap_success(result)
    assert constraint == value


def test_failure_when_minimum_and_maximum_are_unlimited() -> None:
    assert not (result := ranges_between(minimum=UNLIMITED, maximum=UNLIMITED))

    error = unwrap_failure(result)
    assert isinstance(error, UnlimitedRangeError)


def test_failure_when_minimum_and_exclusive_maximum_are_unlimited() -> None:
    assert not (result := ranges_between(minimum=UNLIMITED, exclusive_maximum=UNLIMITED))

    error = unwrap_failure(result)
    assert isinstance(error, UnlimitedRangeError)


def test_failure_when_exclusive_minimum_and_maximum_are_unlimited() -> None:
    assert not (result := ranges_between(exclusive_minimum=UNLIMITED, maximum=UNLIMITED))

    error = unwrap_failure(result)
    assert isinstance(error, UnlimitedRangeError)


def test_failure_when_exclusive_minimum_and_exclusive_maximum_are_unlimited() -> None:
    assert not (result := ranges_between(exclusive_minimum=UNLIMITED, exclusive_maximum=UNLIMITED))

    error = unwrap_failure(result)
    assert isinstance(error, UnlimitedRangeError)


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_above_inclusive_minimum_and_inclusive_maximum(
    data: st.DataObject,
    value: int,
) -> None:
    inclusive_maximum = data.draw(st_value(max_value=value))
    inclusive_minimum = data.draw(st_value(max_value=inclusive_maximum))

    assume(inclusive_maximum != value)
    assume(inclusive_minimum != inclusive_maximum)

    assert (result := ranges_between(minimum=inclusive_minimum, maximum=inclusive_maximum))

    constraint = unwrap_success(result)
    assert constraint != value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_below_inclusive_minimum_and_inclusive_maximum(
    data: st.DataObject,
    value: int,
) -> None:
    inclusive_minimum = data.draw(st_value(min_value=value))
    inclusive_maximum = data.draw(st_value(min_value=inclusive_minimum))

    assume(inclusive_minimum != value)
    assume(inclusive_minimum != inclusive_maximum)

    assert (result := ranges_between(minimum=inclusive_minimum, maximum=inclusive_maximum))

    constraint = unwrap_success(result)
    assert constraint != value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_above_inclusive_minimum_and_exclusive_maximum(
    data: st.DataObject,
    value: int,
) -> None:
    exclusive_maximum = data.draw(st_value(max_value=value))
    inclusive_minimum = data.draw(st_value(max_value=exclusive_maximum))

    assume(inclusive_minimum < exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    assert (
        result := ranges_between(
            minimum=inclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    constraint = unwrap_success(result)
    assert constraint != value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_below_inclusive_minimum_and_exclusive_maximum(
    data: st.DataObject,
    value: int,
) -> None:
    inclusive_minimum = data.draw(st_value(min_value=value))
    exclusive_maximum = data.draw(st_value(min_value=inclusive_minimum))

    assume(inclusive_minimum != value)
    assume(inclusive_minimum < exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    assert (
        result := ranges_between(
            minimum=inclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    constraint = unwrap_success(result)
    assert constraint != value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_above_exclusive_minimum_and_inclusive_maximum(
    data: st.DataObject,
    value: int,
) -> None:
    inclusive_maximum = data.draw(st_value(max_value=value))
    exclusive_minimum = data.draw(st_value(max_value=inclusive_maximum))

    assume(inclusive_maximum != value)
    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT < inclusive_maximum)

    assert (
        result := ranges_between(
            exclusive_minimum=exclusive_minimum,
            maximum=inclusive_maximum,
        )
    )

    constraint = unwrap_success(result)
    assert constraint != value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_below_exclusive_minimum_and_inclusive_maximum(
    data: st.DataObject,
    value: int,
) -> None:
    exclusive_minimum = data.draw(st_value(min_value=value))
    inclusive_maximum = data.draw(st_value(min_value=exclusive_minimum))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT < inclusive_maximum)

    assert (
        result := ranges_between(
            exclusive_minimum=exclusive_minimum,
            maximum=inclusive_maximum,
        )
    )

    constraint = unwrap_success(result)
    assert constraint != value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_above_exclusive_minimum_and_exclusive_maximum(
    data: st.DataObject,
    value: int,
) -> None:
    exclusive_maximum = data.draw(st_value(max_value=value))
    exclusive_minimum = data.draw(st_value(max_value=exclusive_maximum))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT < exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    assert (
        result := ranges_between(
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    constraint = unwrap_success(result)
    assert constraint != value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_below_exclusive_minimum_and_exclusive_maximum(
    data: st.DataObject,
    value: int,
) -> None:
    exclusive_minimum = data.draw(st_value(min_value=value))
    exclusive_maximum = data.draw(st_value(min_value=exclusive_minimum))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT < exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    assert (
        result := ranges_between(
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    constraint = unwrap_success(result)
    assert constraint != value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_not_comparable_with_inclusive_boundaries(
    data: st.DataObject,
    value: int,
) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    assume(inclusive_minimum != inclusive_maximum)

    assert (result := ranges_between(minimum=inclusive_minimum, maximum=inclusive_maximum))

    constraint = unwrap_success(result)
    assert constraint != NotComparable()


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_not_comparable_with_exclusive_boundaries(
    data: st.DataObject,
    value: int,
) -> None:
    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT < exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    assert (
        result := ranges_between(
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    constraint = unwrap_success(result)
    assert constraint != NotComparable()


# noinspection PyArgumentList
def test_failure_when_boundaries_are_missing() -> None:
    assert not (result := ranges_between())

    error = unwrap_failure(result)
    assert isinstance(error, MissingBoundaryError)


# noinspection PyTypeChecker
# noinspection PyArgumentList
@given(data=st.data(), value=st_value())
def test_failure_when_minimum_boundary_is_missing(data: st.DataObject, value: int) -> None:
    inclusive_maximum = data.draw(st_inclusive_maximum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    assert not (result := ranges_between(maximum=inclusive_maximum))

    error = unwrap_failure(result)
    assert isinstance(error, MissingBoundaryError)
    assert error.name == MINIMUM_EXTREMUM

    assert not (result := ranges_between(exclusive_maximum=exclusive_maximum))

    error = unwrap_failure(result)
    assert isinstance(error, MissingBoundaryError)
    assert error.name == MINIMUM_EXTREMUM


# noinspection PyTypeChecker
# noinspection PyArgumentList
@given(data=st.data(), value=st_value())
def test_failure_when_maximum_boundary_is_missing(data: st.DataObject, value: int) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    exclusive_minimum = data.draw(st_exclusive_minimum(value))

    assert not (result := ranges_between(minimum=inclusive_minimum))

    error = unwrap_failure(result)
    assert isinstance(error, MissingBoundaryError)
    assert error.name == MAXIMUM_EXTREMUM

    assert not (result := ranges_between(exclusive_minimum=exclusive_minimum))

    error = unwrap_failure(result)
    assert isinstance(error, MissingBoundaryError)
    assert error.name == MAXIMUM_EXTREMUM


# noinspection PyTypeChecker
# noinspection PyArgumentList
@given(data=st.data(), value=st_value())
def test_failure_when_mutually_exclusive_boundaries_are_set(
    data: st.DataObject,
    value: int,
) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    assert not (
        result := ranges_between(
            minimum=inclusive_minimum,
            maximum=inclusive_maximum,
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    error = unwrap_failure(result)
    assert isinstance(error, MutuallyExclusiveBoundariesError)
    assert error.name == MINIMUM_EXTREMUM


# noinspection PyTypeChecker
# noinspection PyArgumentList
@given(data=st.data(), value=st_value())
def test_failure_when_mutually_exclusive_minimum_boundaries_are_set(
    data: st.DataObject,
    value: int,
) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    assert not (
        result := ranges_between(
            minimum=inclusive_minimum,
            maximum=inclusive_maximum,
            exclusive_minimum=exclusive_minimum,
        )
    )

    error = unwrap_failure(result)
    assert isinstance(error, MutuallyExclusiveBoundariesError)
    assert error.name == MINIMUM_EXTREMUM

    assert not (
        result := ranges_between(
            minimum=inclusive_minimum,
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    error = unwrap_failure(result)
    assert isinstance(error, MutuallyExclusiveBoundariesError)
    assert error.name == MINIMUM_EXTREMUM


# noinspection PyTypeChecker
# noinspection PyArgumentList
@given(data=st.data(), value=st_value())
def test_failure_when_mutually_exclusive_maximum_boundaries_are_set(
    data: st.DataObject,
    value: int,
) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    assert not (
        result := ranges_between(
            minimum=inclusive_minimum,
            maximum=inclusive_maximum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    error = unwrap_failure(result)
    assert isinstance(error, MutuallyExclusiveBoundariesError)
    assert error.name == MAXIMUM_EXTREMUM

    assert not (
        result := ranges_between(
            maximum=inclusive_maximum,
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    error = unwrap_failure(result)
    assert isinstance(error, MutuallyExclusiveBoundariesError)
    assert error.name == MAXIMUM_EXTREMUM


# noinspection PyTypeChecker
@given(data=st.data())
def test_failure_when_inclusive_minimum_and_inclusive_maximum_are_overlapping(
    data: st.DataObject,
) -> None:
    inclusive_minimum = data.draw(st_value())
    inclusive_maximum = data.draw(st_value(max_value=inclusive_minimum))

    assume(inclusive_minimum != inclusive_maximum)

    assert not (
        result := ranges_between(
            minimum=inclusive_minimum,
            maximum=inclusive_maximum,
        )
    )

    error = unwrap_failure(result)
    assert isinstance(error, OverlappingBoundariesError)
    assert error.minimum.value == inclusive_minimum
    assert error.minimum.is_inclusive is True
    assert error.maximum.value == inclusive_maximum
    assert error.maximum.is_inclusive is True


# noinspection PyTypeChecker
@given(data=st.data())
def test_failure_when_inclusive_minimum_and_exclusive_maximum_are_overlapping(
    data: st.DataObject,
) -> None:
    inclusive_minimum = data.draw(st_value())
    exclusive_maximum = data.draw(st_value(max_value=inclusive_minimum))

    assert not (
        result := ranges_between(
            minimum=inclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    error = unwrap_failure(result)
    assert isinstance(error, OverlappingBoundariesError)
    assert error.minimum.value == inclusive_minimum
    assert error.minimum.is_inclusive is True
    assert error.maximum.value == exclusive_maximum
    assert error.maximum.is_inclusive is False


# noinspection PyTypeChecker
@given(data=st.data())
def test_failure_when_exclusive_minimum_and_inclusive_maximum_are_overlapping(
    data: st.DataObject,
) -> None:
    exclusive_minimum = data.draw(st_value())
    inclusive_maximum = data.draw(st_value(max_value=exclusive_minimum))

    assert not (
        result := ranges_between(
            exclusive_minimum=exclusive_minimum,
            maximum=inclusive_maximum,
        )
    )

    error = unwrap_failure(result)
    assert isinstance(error, OverlappingBoundariesError)
    assert error.minimum.value == exclusive_minimum
    assert error.minimum.is_inclusive is False
    assert error.maximum.value == inclusive_maximum
    assert error.maximum.is_inclusive is True


# noinspection PyTypeChecker
@given(data=st.data())
def test_failure_when_exclusive_minimum_and_exclusive_maximum_are_overlapping(
    data: st.DataObject,
) -> None:
    exclusive_minimum = data.draw(st_value())
    exclusive_maximum = data.draw(st_value(max_value=exclusive_minimum + EXCLUSIVE_ALIGNMENT))

    assert not (
        result := ranges_between(
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    error = unwrap_failure(result)
    assert isinstance(error, OverlappingBoundariesError)
    assert error.minimum.value == exclusive_minimum
    assert error.minimum.is_inclusive is False
    assert error.maximum.value == exclusive_maximum
    assert error.maximum.is_inclusive is False


# noinspection PyTypeChecker
@given(value=st_value())
def test_failure_when_inclusive_minimum_and_inclusive_maximum_match_single_value(
    value: int,
) -> None:
    inclusive_minimum = value
    inclusive_maximum = value

    assert not (
        result := ranges_between(
            minimum=inclusive_minimum,
            maximum=inclusive_maximum,
        )
    )

    error = unwrap_failure(result)
    assert isinstance(error, SingleMatchBoundariesError)
    assert error.minimum.value == inclusive_minimum
    assert error.minimum.is_inclusive is True
    assert error.maximum.value == inclusive_maximum
    assert error.maximum.is_inclusive is True


# noinspection PyTypeChecker
@given(value=st_value())
def test_failure_when_inclusive_minimum_and_exclusive_maximum_match_single_value(
    value: int,
) -> None:
    inclusive_minimum = value
    exclusive_maximum = value + EXCLUSIVE_ALIGNMENT

    assert not (
        result := ranges_between(
            minimum=inclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    error = unwrap_failure(result)
    assert isinstance(error, SingleMatchBoundariesError)
    assert error.minimum.value == inclusive_minimum
    assert error.minimum.is_inclusive is True
    assert error.maximum.value == exclusive_maximum
    assert error.maximum.is_inclusive is False


# noinspection PyTypeChecker
@given(value=st_value())
def test_failure_when_exclusive_minimum_and_inclusive_maximum_match_single_value(
    value: int,
) -> None:
    exclusive_minimum = value - EXCLUSIVE_ALIGNMENT
    inclusive_maximum = value

    assert not (
        result := ranges_between(
            exclusive_minimum=exclusive_minimum,
            maximum=inclusive_maximum,
        )
    )

    error = unwrap_failure(result)
    assert isinstance(error, SingleMatchBoundariesError)
    assert error.minimum.value == exclusive_minimum
    assert error.minimum.is_inclusive is False
    assert error.maximum.value == inclusive_maximum
    assert error.maximum.is_inclusive is True


# noinspection PyTypeChecker
@given(value=st_value())
def test_failure_when_exclusive_minimum_and_exclusive_maximum_match_single_value(
    value: int,
) -> None:
    exclusive_minimum = value - EXCLUSIVE_ALIGNMENT
    exclusive_maximum = value + EXCLUSIVE_ALIGNMENT

    assert not (
        result := ranges_between(
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    error = unwrap_failure(result)
    assert isinstance(error, SingleMatchBoundariesError)
    assert error.minimum.value == exclusive_minimum
    assert error.minimum.is_inclusive is False
    assert error.maximum.value == exclusive_maximum
    assert error.maximum.is_inclusive is False
