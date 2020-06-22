from typing import Any, Optional, Final

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import ranges_between

from tests.conftest import Draw

EXCLUSIVE_ALIGNMENT: Final[int] = 1


class NotImplementedBoundaries:

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


@given(data=st.data(), value=st_value())
def test_repr_with_inclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    fmt = "testplates.ranges_between(minimum={minimum}, maximum={maximum})"

    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    assume(inclusive_minimum != inclusive_maximum)

    constraint = ranges_between(minimum=inclusive_minimum, maximum=inclusive_maximum)

    assert repr(constraint) == fmt.format(minimum=inclusive_minimum, maximum=inclusive_maximum)


@given(data=st.data(), value=st_value())
def test_repr_with_inclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    fmt = "testplates.ranges_between(minimum={minimum}, exclusive_maximum={maximum})"

    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    assume(inclusive_minimum != exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    constraint = ranges_between(minimum=inclusive_minimum, exclusive_maximum=exclusive_maximum)

    assert repr(constraint) == fmt.format(minimum=inclusive_minimum, maximum=exclusive_maximum)


@given(data=st.data(), value=st_value())
def test_repr_with_exclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    fmt = "testplates.ranges_between(exclusive_minimum={minimum}, maximum={maximum})"

    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT != inclusive_maximum)

    constraint = ranges_between(exclusive_minimum=exclusive_minimum, maximum=inclusive_maximum)

    assert repr(constraint) == fmt.format(minimum=exclusive_minimum, maximum=inclusive_maximum)


@given(data=st.data(), value=st_value())
def test_repr_with_exclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    fmt = "testplates.ranges_between(exclusive_minimum={minimum}, exclusive_maximum={maximum})"

    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT != exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    constraint = ranges_between(
        exclusive_minimum=exclusive_minimum, exclusive_maximum=exclusive_maximum
    )

    assert repr(constraint) == fmt.format(minimum=exclusive_minimum, maximum=exclusive_maximum)


@given(data=st.data(), value=st_value())
def test_returns_true_with_inclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    assume(inclusive_minimum != inclusive_maximum)

    constraint = ranges_between(minimum=inclusive_minimum, maximum=inclusive_maximum)

    assert constraint == value


@given(data=st.data(), value=st_value())
def test_returns_true_with_inclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    assume(inclusive_minimum != exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    constraint = ranges_between(minimum=inclusive_minimum, exclusive_maximum=exclusive_maximum)

    assert constraint == value


@given(data=st.data(), value=st_value())
def test_returns_true_with_exclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT != inclusive_maximum)

    constraint = ranges_between(exclusive_minimum=exclusive_minimum, maximum=inclusive_maximum)

    assert constraint == value


@given(data=st.data(), value=st_value())
def test_returns_true_with_exclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT != exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    constraint = ranges_between(
        exclusive_minimum=exclusive_minimum, exclusive_maximum=exclusive_maximum
    )

    assert constraint == value


@given(data=st.data(), value=st_value())
def test_returns_false_with_upper_inclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st_value(min_value=value))
    inclusive_maximum = data.draw(st_value(min_value=inclusive_minimum))

    assume(inclusive_minimum != value)
    assume(inclusive_minimum != inclusive_maximum)

    constraint = ranges_between(minimum=inclusive_minimum, maximum=inclusive_maximum)

    assert constraint != value


@given(data=st.data(), value=st_value())
def test_returns_false_with_lower_inclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    inclusive_maximum = data.draw(st_value(max_value=value))
    inclusive_minimum = data.draw(st_value(max_value=inclusive_maximum))

    assume(inclusive_maximum != value)
    assume(inclusive_minimum != inclusive_maximum)

    constraint = ranges_between(minimum=inclusive_minimum, maximum=inclusive_maximum)

    assert constraint != value


@given(data=st.data(), value=st_value())
def test_returns_false_with_upper_inclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st_value(min_value=value))
    exclusive_maximum = data.draw(st_value(min_value=inclusive_minimum))

    assume(inclusive_minimum != value)
    assume(inclusive_minimum < exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    constraint = ranges_between(minimum=inclusive_minimum, exclusive_maximum=exclusive_maximum)

    assert constraint != value


@given(data=st.data(), value=st_value())
def test_returns_false_with_lower_inclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    exclusive_maximum = data.draw(st_value(max_value=value))
    inclusive_minimum = data.draw(st_value(max_value=exclusive_maximum))

    assume(exclusive_maximum != value)
    assume(inclusive_minimum < exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    constraint = ranges_between(minimum=inclusive_minimum, exclusive_maximum=exclusive_maximum)

    assert constraint != value


@given(data=st.data(), value=st_value())
def test_returns_false_with_upper_exclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    exclusive_minimum = data.draw(st_value(min_value=value))
    inclusive_maximum = data.draw(st_value(min_value=exclusive_minimum))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT < inclusive_maximum)

    constraint = ranges_between(exclusive_minimum=exclusive_minimum, maximum=inclusive_maximum)

    assert constraint != value


@given(data=st.data(), value=st_value())
def test_returns_false_with_lower_exclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    inclusive_maximum = data.draw(st_value(max_value=value))
    exclusive_minimum = data.draw(st_value(max_value=inclusive_maximum))

    assume(inclusive_maximum != value)
    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT < inclusive_maximum)

    constraint = ranges_between(exclusive_minimum=exclusive_minimum, maximum=inclusive_maximum)

    assert constraint != value


@given(data=st.data(), value=st_value())
def test_returns_false_with_upper_exclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    exclusive_minimum = data.draw(st_value(min_value=value))
    exclusive_maximum = data.draw(st_value(min_value=exclusive_minimum))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT < exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    constraint = ranges_between(
        exclusive_minimum=exclusive_minimum, exclusive_maximum=exclusive_maximum
    )

    assert constraint != value


@given(data=st.data(), value=st_value())
def test_returns_false_with_lower_exclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    exclusive_maximum = data.draw(st_value(max_value=value))
    exclusive_minimum = data.draw(st_value(max_value=exclusive_maximum))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT < exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    constraint = ranges_between(
        exclusive_minimum=exclusive_minimum, exclusive_maximum=exclusive_maximum
    )

    assert constraint != value


@given(data=st.data(), value=st_value())
def test_returns_false_when_value_does_not_implement_boundaries_with_inclusive_boundaries(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    assume(inclusive_minimum != inclusive_maximum)

    constraint = ranges_between(minimum=inclusive_minimum, maximum=inclusive_maximum)

    assert constraint != NotImplementedBoundaries()


@given(data=st.data(), value=st_value())
def test_returns_false_when_value_does_not_implement_boundaries_with_exclusive_boundaries(
    data: st.DataObject, value: int
) -> None:
    exclusive_minimum = data.draw(st_inclusive_minimum(value))
    exclusive_maximum = data.draw(st_inclusive_maximum(value))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT < exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    constraint = ranges_between(
        exclusive_minimum=exclusive_minimum, exclusive_maximum=exclusive_maximum
    )

    assert constraint != NotImplementedBoundaries()
