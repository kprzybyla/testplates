from typing import Any, Optional, Final

import pytest

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import UNLIMITED
from testplates import (
    ranges_between,
    MissingBoundaryError,
    MutuallyExclusiveBoundariesError,
    OverlappingBoundariesError,
    SingleMatchBoundariesError,
)

from tests.conftest import Draw

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
    draw: Draw[int], min_value: Optional[int] = None, max_value: Optional[int] = None
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
    data: st.DataObject, value: int
) -> None:
    fmt = "testplates.RangesBetween(minimum={minimum}, maximum={maximum})"

    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    assume(inclusive_minimum != inclusive_maximum)

    constraint = ranges_between(minimum=inclusive_minimum, maximum=inclusive_maximum)

    assert repr(constraint) == fmt.format(minimum=inclusive_minimum, maximum=inclusive_maximum)


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_repr_with_inclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    fmt = "testplates.RangesBetween(minimum={minimum}, exclusive_maximum={maximum})"

    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    assume(inclusive_minimum != exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    constraint = ranges_between(minimum=inclusive_minimum, exclusive_maximum=exclusive_maximum)

    assert repr(constraint) == fmt.format(minimum=inclusive_minimum, maximum=exclusive_maximum)


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_repr_with_exclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    fmt = "testplates.RangesBetween(exclusive_minimum={minimum}, maximum={maximum})"

    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT != inclusive_maximum)

    constraint = ranges_between(exclusive_minimum=exclusive_minimum, maximum=inclusive_maximum)

    assert repr(constraint) == fmt.format(minimum=exclusive_minimum, maximum=inclusive_maximum)


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_repr_with_exclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    fmt = "testplates.RangesBetween(exclusive_minimum={minimum}, exclusive_maximum={maximum})"

    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT != exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    constraint = ranges_between(
        exclusive_minimum=exclusive_minimum, exclusive_maximum=exclusive_maximum
    )

    assert repr(constraint) == fmt.format(minimum=exclusive_minimum, maximum=exclusive_maximum)


# noinspection PyTypeChecker
@given(value=st_value())
def test_success_with_unlimited_minimum_and_unlimited_maximum(value: int) -> None:
    constraint = ranges_between(minimum=UNLIMITED, maximum=UNLIMITED)

    assert constraint == value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_success_with_inclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    assume(inclusive_minimum != inclusive_maximum)

    constraint = ranges_between(minimum=inclusive_minimum, maximum=inclusive_maximum)

    assert constraint == value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_success_with_inclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    assume(inclusive_minimum != exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    constraint = ranges_between(minimum=inclusive_minimum, exclusive_maximum=exclusive_maximum)

    assert constraint == value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_success_with_exclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT != inclusive_maximum)

    constraint = ranges_between(exclusive_minimum=exclusive_minimum, maximum=inclusive_maximum)

    assert constraint == value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_success_with_exclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT != exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    constraint = ranges_between(
        exclusive_minimum=exclusive_minimum, exclusive_maximum=exclusive_maximum
    )

    assert constraint == value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_above_inclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    inclusive_maximum = data.draw(st_value(max_value=value))
    inclusive_minimum = data.draw(st_value(max_value=inclusive_maximum))

    assume(inclusive_maximum != value)
    assume(inclusive_minimum != inclusive_maximum)

    constraint = ranges_between(minimum=inclusive_minimum, maximum=inclusive_maximum)

    assert constraint != value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_below_inclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st_value(min_value=value))
    inclusive_maximum = data.draw(st_value(min_value=inclusive_minimum))

    assume(inclusive_minimum != value)
    assume(inclusive_minimum != inclusive_maximum)

    constraint = ranges_between(minimum=inclusive_minimum, maximum=inclusive_maximum)

    assert constraint != value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_above_inclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    exclusive_maximum = data.draw(st_value(max_value=value))
    inclusive_minimum = data.draw(st_value(max_value=exclusive_maximum))

    assume(inclusive_minimum < exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    constraint = ranges_between(minimum=inclusive_minimum, exclusive_maximum=exclusive_maximum)

    assert constraint != value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_below_inclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st_value(min_value=value))
    exclusive_maximum = data.draw(st_value(min_value=inclusive_minimum))

    assume(inclusive_minimum != value)
    assume(inclusive_minimum < exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    constraint = ranges_between(minimum=inclusive_minimum, exclusive_maximum=exclusive_maximum)

    assert constraint != value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_above_exclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    inclusive_maximum = data.draw(st_value(max_value=value))
    exclusive_minimum = data.draw(st_value(max_value=inclusive_maximum))

    assume(inclusive_maximum != value)
    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT < inclusive_maximum)

    constraint = ranges_between(exclusive_minimum=exclusive_minimum, maximum=inclusive_maximum)

    assert constraint != value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_below_exclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    exclusive_minimum = data.draw(st_value(min_value=value))
    inclusive_maximum = data.draw(st_value(min_value=exclusive_minimum))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT < inclusive_maximum)

    constraint = ranges_between(exclusive_minimum=exclusive_minimum, maximum=inclusive_maximum)

    assert constraint != value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_above_exclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    exclusive_maximum = data.draw(st_value(max_value=value))
    exclusive_minimum = data.draw(st_value(max_value=exclusive_maximum))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT < exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    constraint = ranges_between(
        exclusive_minimum=exclusive_minimum, exclusive_maximum=exclusive_maximum
    )

    assert constraint != value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_below_exclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    exclusive_minimum = data.draw(st_value(min_value=value))
    exclusive_maximum = data.draw(st_value(min_value=exclusive_minimum))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT < exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    constraint = ranges_between(
        exclusive_minimum=exclusive_minimum, exclusive_maximum=exclusive_maximum
    )

    assert constraint != value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_not_comparable_with_inclusive_boundaries(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    assume(inclusive_minimum != inclusive_maximum)

    constraint = ranges_between(minimum=inclusive_minimum, maximum=inclusive_maximum)

    assert constraint != NotComparable()


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_not_comparable_with_exclusive_boundaries(
    data: st.DataObject, value: int
) -> None:
    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT < exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    constraint = ranges_between(
        exclusive_minimum=exclusive_minimum, exclusive_maximum=exclusive_maximum
    )

    assert constraint != NotComparable()


# noinspection PyArgumentList
def test_failure_when_boundaries_are_missing() -> None:
    with pytest.raises(TypeError):
        ranges_between()  # type: ignore


# noinspection PyTypeChecker
# noinspection PyArgumentList
@given(data=st.data(), value=st_value())
def test_failure_when_minimum_boundary_is_missing(data: st.DataObject, value: int) -> None:
    inclusive_maximum = data.draw(st_inclusive_maximum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    with pytest.raises(MissingBoundaryError):
        ranges_between(maximum=inclusive_maximum)

    with pytest.raises(MissingBoundaryError):
        ranges_between(exclusive_maximum=exclusive_maximum)


# noinspection PyTypeChecker
# noinspection PyArgumentList
@given(data=st.data(), value=st_value())
def test_failure_when_maximum_boundary_is_missing(data: st.DataObject, value: int) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    exclusive_minimum = data.draw(st_exclusive_minimum(value))

    with pytest.raises(MissingBoundaryError):
        ranges_between(minimum=inclusive_minimum)

    with pytest.raises(MissingBoundaryError):
        ranges_between(exclusive_minimum=exclusive_minimum)


# noinspection PyTypeChecker
# noinspection PyArgumentList
@given(data=st.data(), value=st_value())
def test_failure_when_mutually_exclusive_boundaries_are_set(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    with pytest.raises(MutuallyExclusiveBoundariesError):
        ranges_between(
            minimum=inclusive_minimum,
            maximum=inclusive_maximum,
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )


# noinspection PyTypeChecker
# noinspection PyArgumentList
@given(data=st.data(), value=st_value())
def test_failure_when_mutually_exclusive_minimum_boundaries_are_set(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    with pytest.raises(MutuallyExclusiveBoundariesError):
        ranges_between(
            minimum=inclusive_minimum,
            maximum=inclusive_maximum,
            exclusive_minimum=exclusive_minimum,
        )

    with pytest.raises(MutuallyExclusiveBoundariesError):
        ranges_between(
            minimum=inclusive_minimum,
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )


# noinspection PyTypeChecker
# noinspection PyArgumentList
@given(data=st.data(), value=st_value())
def test_failure_when_mutually_exclusive_maximum_boundaries_are_set(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    with pytest.raises(MutuallyExclusiveBoundariesError):
        ranges_between(
            minimum=inclusive_minimum,
            maximum=inclusive_maximum,
            exclusive_maximum=exclusive_maximum,
        )

    with pytest.raises(MutuallyExclusiveBoundariesError):
        ranges_between(
            maximum=inclusive_maximum,
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )


# noinspection PyTypeChecker
@given(data=st.data())
def test_failure_when_inclusive_minimum_and_inclusive_maximum_are_overlapping(
    data: st.DataObject,
) -> None:
    inclusive_minimum = data.draw(st_value())
    inclusive_maximum = data.draw(st_value(max_value=inclusive_minimum))

    assume(inclusive_minimum != inclusive_maximum)

    with pytest.raises(OverlappingBoundariesError):
        ranges_between(minimum=inclusive_minimum, maximum=inclusive_maximum)


# noinspection PyTypeChecker
@given(data=st.data())
def test_failure_when_inclusive_minimum_and_exclusive_maximum_are_overlapping(
    data: st.DataObject,
) -> None:
    inclusive_minimum = data.draw(st_value())
    exclusive_maximum = data.draw(st_value(max_value=inclusive_minimum))

    with pytest.raises(OverlappingBoundariesError):
        ranges_between(minimum=inclusive_minimum, exclusive_maximum=exclusive_maximum)


# noinspection PyTypeChecker
@given(data=st.data())
def test_failure_when_exclusive_minimum_and_inclusive_maximum_are_overlapping(
    data: st.DataObject,
) -> None:
    exclusive_minimum = data.draw(st_value())
    inclusive_maximum = data.draw(st_value(max_value=exclusive_minimum))

    with pytest.raises(OverlappingBoundariesError):
        ranges_between(exclusive_minimum=exclusive_minimum, maximum=inclusive_maximum)


# noinspection PyTypeChecker
@given(data=st.data())
def test_failure_when_exclusive_minimum_and_exclusive_maximum_are_overlapping(
    data: st.DataObject,
) -> None:
    exclusive_minimum = data.draw(st_value())
    exclusive_maximum = data.draw(st_value(max_value=exclusive_minimum + EXCLUSIVE_ALIGNMENT))

    with pytest.raises(OverlappingBoundariesError):
        ranges_between(exclusive_minimum=exclusive_minimum, exclusive_maximum=exclusive_maximum)


@given(value=st_value())
def test_failure_when_inclusive_minimum_and_inclusive_maximum_match_single_value(
    value: int,
) -> None:
    inclusive_minimum = value
    inclusive_maximum = value

    with pytest.raises(SingleMatchBoundariesError):
        ranges_between(minimum=inclusive_minimum, maximum=inclusive_maximum)


@given(value=st_value())
def test_failure_when_inclusive_minimum_and_exclusive_maximum_match_single_value(
    value: int,
) -> None:
    inclusive_minimum = value
    exclusive_maximum = value + EXCLUSIVE_ALIGNMENT

    with pytest.raises(SingleMatchBoundariesError):
        ranges_between(minimum=inclusive_minimum, exclusive_maximum=exclusive_maximum)


@given(value=st_value())
def test_failure_when_exclusive_minimum_and_inclusive_maximum_match_single_value(
    value: int,
) -> None:
    exclusive_minimum = value - EXCLUSIVE_ALIGNMENT
    inclusive_maximum = value

    with pytest.raises(SingleMatchBoundariesError):
        ranges_between(exclusive_minimum=exclusive_minimum, maximum=inclusive_maximum)


@given(value=st_value())
def test_failure_when_exclusive_minimum_and_exclusive_maximum_match_single_value(
    value: int,
) -> None:
    exclusive_minimum = value - EXCLUSIVE_ALIGNMENT
    exclusive_maximum = value + EXCLUSIVE_ALIGNMENT

    with pytest.raises(SingleMatchBoundariesError):
        ranges_between(exclusive_minimum=exclusive_minimum, exclusive_maximum=exclusive_maximum)
