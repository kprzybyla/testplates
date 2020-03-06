from typing import Optional
from typing_extensions import Final

import pytest

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import (
    ranges_between,
    MissingBoundaryError,
    MutuallyExclusiveBoundariesError,
    OverlappingBoundariesError,
    SingleMatchBoundariesError,
)

from ..conftest import Draw

EXCLUSIVE_ALIGNMENT: Final[int] = 1


class NotImplementedBoundaries:

    __slots__ = ()

    def __gt__(self, other):
        return NotImplemented

    def __lt__(self, other):
        return NotImplemented

    def __ge__(self, other):
        return NotImplemented

    def __le__(self, other):
        return NotImplemented


@st.composite
def st_value(draw: Draw, min_value: Optional[int] = None, max_value: Optional[int] = None) -> int:
    return draw(st.integers(min_value=min_value, max_value=max_value))


@st.composite
def st_inclusive_minimum(draw: Draw, value: int) -> int:
    return draw(st.integers(max_value=value))


@st.composite
def st_inclusive_maximum(draw: Draw, value: int) -> int:
    return draw(st.integers(min_value=value))


@st.composite
def st_exclusive_minimum(draw: Draw, value: int) -> int:
    minimum = draw(st_inclusive_minimum(value))
    assume(value != minimum)

    return minimum


@st.composite
def st_exclusive_maximum(draw: Draw, value: int) -> int:
    maximum = draw(st_inclusive_maximum(value))
    assume(value != maximum)

    return maximum


@given(data=st.data(), value=st_value())
def test_returns_true_with_inclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    assume(inclusive_minimum != inclusive_maximum)

    template = ranges_between(minimum=inclusive_minimum, maximum=inclusive_maximum)

    assert template == value


@given(data=st.data(), value=st_value())
def test_returns_true_with_inclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    assume(inclusive_minimum != exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    template = ranges_between(minimum=inclusive_minimum, exclusive_maximum=exclusive_maximum)

    assert template == value


@given(data=st.data(), value=st_value())
def test_returns_true_with_exclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT != inclusive_maximum)

    template = ranges_between(exclusive_minimum=exclusive_minimum, maximum=inclusive_maximum)

    assert template == value


@given(data=st.data(), value=st_value())
def test_returns_true_with_exclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT != exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    template = ranges_between(
        exclusive_minimum=exclusive_minimum, exclusive_maximum=exclusive_maximum
    )

    assert template == value


@given(data=st.data(), value=st_value())
def test_returns_false_with_upper_inclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st_value(min_value=value))
    inclusive_maximum = data.draw(st_value(min_value=inclusive_minimum))

    assume(inclusive_minimum != value)
    assume(inclusive_minimum != inclusive_maximum)

    template = ranges_between(minimum=inclusive_minimum, maximum=inclusive_maximum)

    assert template != value


@given(data=st.data(), value=st_value())
def test_returns_false_with_lower_inclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    inclusive_maximum = data.draw(st_value(max_value=value))
    inclusive_minimum = data.draw(st_value(max_value=inclusive_maximum))

    assume(inclusive_maximum != value)
    assume(inclusive_minimum != inclusive_maximum)

    template = ranges_between(minimum=inclusive_minimum, maximum=inclusive_maximum)

    assert template != value


@given(data=st.data(), value=st_value())
def test_returns_false_with_upper_inclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st_value(min_value=value))
    exclusive_maximum = data.draw(st_value(min_value=inclusive_minimum))

    assume(inclusive_minimum != value)
    assume(inclusive_minimum < exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    template = ranges_between(minimum=inclusive_minimum, exclusive_maximum=exclusive_maximum)

    assert template != value


@given(data=st.data(), value=st_value())
def test_returns_false_with_lower_inclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    exclusive_maximum = data.draw(st_value(max_value=value))
    inclusive_minimum = data.draw(st_value(max_value=exclusive_maximum))

    assume(exclusive_maximum != value)
    assume(inclusive_minimum < exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    template = ranges_between(minimum=inclusive_minimum, exclusive_maximum=exclusive_maximum)

    assert template != value


@given(data=st.data(), value=st_value())
def test_returns_false_with_upper_exclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    exclusive_minimum = data.draw(st_value(min_value=value))
    inclusive_maximum = data.draw(st_value(min_value=exclusive_minimum))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT < inclusive_maximum)

    template = ranges_between(exclusive_minimum=exclusive_minimum, maximum=inclusive_maximum)

    assert template != value


@given(data=st.data(), value=st_value())
def test_returns_false_with_lower_exclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    inclusive_maximum = data.draw(st_value(max_value=value))
    exclusive_minimum = data.draw(st_value(max_value=inclusive_maximum))

    assume(inclusive_maximum != value)
    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT < inclusive_maximum)

    template = ranges_between(exclusive_minimum=exclusive_minimum, maximum=inclusive_maximum)

    assert template != value


@given(data=st.data(), value=st_value())
def test_returns_false_with_upper_exclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    exclusive_minimum = data.draw(st_value(min_value=value))
    exclusive_maximum = data.draw(st_value(min_value=exclusive_minimum))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT < exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    template = ranges_between(
        exclusive_minimum=exclusive_minimum, exclusive_maximum=exclusive_maximum
    )

    assert template != value


@given(data=st.data(), value=st_value())
def test_returns_false_with_lower_exclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    exclusive_maximum = data.draw(st_value(max_value=value))
    exclusive_minimum = data.draw(st_value(max_value=exclusive_maximum))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT < exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    template = ranges_between(
        exclusive_minimum=exclusive_minimum, exclusive_maximum=exclusive_maximum
    )

    assert template != value


@given(data=st.data(), value=st_value())
def test_returns_false_when_value_does_not_implement_boundaries_with_inclusive_boundaries(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    assume(inclusive_minimum != inclusive_maximum)

    template = ranges_between(minimum=inclusive_minimum, maximum=inclusive_maximum)

    assert template != NotImplementedBoundaries()


@given(data=st.data(), value=st_value())
def test_returns_false_when_value_does_not_implement_boundaries_with_exclusive_boundaries(
    data: st.DataObject, value: int
) -> None:
    exclusive_minimum = data.draw(st_inclusive_minimum(value))
    exclusive_maximum = data.draw(st_inclusive_maximum(value))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT < exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    template = ranges_between(
        exclusive_minimum=exclusive_minimum, exclusive_maximum=exclusive_maximum
    )

    assert template != NotImplementedBoundaries()


# noinspection PyArgumentList
def test_raises_error_on_missing_boundaries() -> None:
    with pytest.raises(TypeError):
        ranges_between()


# noinspection PyArgumentList
@given(data=st.data(), value=st_value())
def test_raises_error_on_missing_minimum_boundary(data: st.DataObject, value: int) -> None:
    inclusive_maximum = data.draw(st_inclusive_maximum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    with pytest.raises(MissingBoundaryError):
        ranges_between(maximum=inclusive_maximum)

    with pytest.raises(MissingBoundaryError):
        ranges_between(exclusive_maximum=exclusive_maximum)


# noinspection PyArgumentList
@given(data=st.data(), value=st_value())
def test_raises_error_on_missing_maximum_boundary(data: st.DataObject, value: int) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    exclusive_minimum = data.draw(st_exclusive_minimum(value))

    with pytest.raises(MissingBoundaryError):
        ranges_between(minimum=inclusive_minimum)

    with pytest.raises(MissingBoundaryError):
        ranges_between(exclusive_minimum=exclusive_minimum)


# noinspection PyArgumentList
@given(data=st.data(), value=st_value())
def test_raises_error_on_mutually_exclusive_boundaries(data: st.DataObject, value: int) -> None:
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

    with pytest.raises(MutuallyExclusiveBoundariesError):
        ranges_between(
            minimum=inclusive_minimum,
            maximum=inclusive_maximum,
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )


@given(data=st.data(), value=st_value())
def test_raises_error_on_inclusive_minimum_and_inclusive_maximum_overlapping(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st_value())
    inclusive_maximum = data.draw(st_value(max_value=inclusive_minimum))

    assume(inclusive_minimum != inclusive_maximum)

    with pytest.raises(OverlappingBoundariesError):
        ranges_between(minimum=inclusive_minimum, maximum=inclusive_maximum)


@given(data=st.data(), value=st_value())
def test_raises_error_on_inclusive_minimum_and_exclusive_maximum_overlapping(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st_value())
    exclusive_maximum = data.draw(st_value(max_value=inclusive_minimum))

    with pytest.raises(OverlappingBoundariesError):
        ranges_between(minimum=inclusive_minimum, exclusive_maximum=exclusive_maximum)


@given(data=st.data(), value=st_value())
def test_raises_error_on_exclusive_minimum_and_inclusive_maximum_overlapping(
    data: st.DataObject, value: int
) -> None:
    exclusive_minimum = data.draw(st_value())
    inclusive_maximum = data.draw(st_value(max_value=exclusive_minimum))

    with pytest.raises(OverlappingBoundariesError):
        ranges_between(exclusive_minimum=exclusive_minimum, maximum=inclusive_maximum)


@given(data=st.data(), value=st_value())
def test_raises_error_on_exclusive_minimum_and_exclusive_maximum_overlapping(
    data: st.DataObject, value: int
) -> None:
    exclusive_minimum = data.draw(st_value())
    exclusive_maximum = data.draw(st_value(max_value=exclusive_minimum + EXCLUSIVE_ALIGNMENT))

    with pytest.raises(OverlappingBoundariesError):
        ranges_between(exclusive_minimum=exclusive_minimum, exclusive_maximum=exclusive_maximum)


@given(value=st_value())
def test_raises_error_on_single_match_with_inclusive_minimum_and_inclusive_maximum(
    value: int
) -> None:
    inclusive_minimum = value
    inclusive_maximum = value

    with pytest.raises(SingleMatchBoundariesError):
        ranges_between(minimum=inclusive_minimum, maximum=inclusive_maximum)


@given(value=st_value())
def test_raises_error_on_single_match_with_inclusive_minimum_and_exclusive_maximum(
    value: int
) -> None:
    inclusive_minimum = value
    exclusive_maximum = value + EXCLUSIVE_ALIGNMENT

    with pytest.raises(SingleMatchBoundariesError):
        ranges_between(minimum=inclusive_minimum, exclusive_maximum=exclusive_maximum)


@given(value=st_value())
def test_raises_error_on_single_match_with_exclusive_minimum_and_inclusive_maximum(
    value: int
) -> None:
    exclusive_minimum = value - EXCLUSIVE_ALIGNMENT
    inclusive_maximum = value

    with pytest.raises(SingleMatchBoundariesError):
        ranges_between(exclusive_minimum=exclusive_minimum, maximum=inclusive_maximum)


@given(value=st_value())
def test_raises_error_on_single_match_with_exclusive_minimum_and_exclusive_maximum(
    value: int
) -> None:
    exclusive_minimum = value - EXCLUSIVE_ALIGNMENT
    exclusive_maximum = value + EXCLUSIVE_ALIGNMENT

    with pytest.raises(SingleMatchBoundariesError):
        ranges_between(exclusive_minimum=exclusive_minimum, exclusive_maximum=exclusive_maximum)
