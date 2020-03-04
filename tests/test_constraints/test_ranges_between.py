from typing import Optional
from functools import partial

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


@st.composite
def st_value(draw: Draw, max_value: Optional[int] = None) -> int:
    return draw(st.integers(max_value=max_value))


@st.composite
def st_inclusive_minimum(draw: Draw, value: int) -> int:
    return draw(st.integers(max_value=value))


@st.composite
def st_inclusive_maximum(draw: Draw, value: int) -> int:
    return draw(st.integers(min_value=value))


@st.composite
def st_exclusive_minimum(draw: Draw, value: int) -> int:
    minimum = draw(st_inclusive_minimum(value))
    assume(minimum < value)

    return minimum


@st.composite
def st_exclusive_maximum(draw: Draw, value: int) -> int:
    maximum = draw(st_inclusive_maximum(value))
    assume(value < maximum)

    return maximum


@given(data=st.data(), value=st_value())
def test_constraint_returns_true_with_inclusive_minimum_and_maximum(
    data: st.DataObject, value: int
):
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    assume(inclusive_minimum != inclusive_maximum)

    template = ranges_between(minimum=inclusive_minimum, maximum=inclusive_maximum)

    assert template == value


@given(data=st.data(), value=st_value())
def test_constraint_returns_true_with_inclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, value: int
):
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    assume(inclusive_minimum < exclusive_maximum - 1)

    template = ranges_between(minimum=inclusive_minimum, exclusive_maximum=exclusive_maximum)

    assert template == value


@given(data=st.data(), value=st_value())
def test_constraint_returns_true_with_exclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, value: int
):
    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    assume(exclusive_minimum + 1 < inclusive_maximum)

    template = ranges_between(exclusive_minimum=exclusive_minimum, maximum=inclusive_maximum)

    assert template == value


@given(data=st.data(), value=st_value())
def test_constraint_returns_true_with_exclusive_minimum_and_maximum(
    data: st.DataObject, value: int
):
    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    assume(exclusive_minimum + 1 < exclusive_maximum - 1)

    template = ranges_between(
        exclusive_minimum=exclusive_minimum, exclusive_maximum=exclusive_maximum
    )

    assert template == value


@given(data=st.data(), value=st_value())
def test_constraint_returns_false_with_upper_inclusive_boundaries(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st.integers(min_value=value))
    inclusive_maximum = data.draw(st.integers(min_value=inclusive_minimum))

    assume(inclusive_minimum != value)
    assume(inclusive_minimum != inclusive_maximum)

    template = ranges_between(minimum=inclusive_minimum, maximum=inclusive_maximum)

    assert template != value


@given(data=st.data(), value=st_value())
def test_constraint_returns_false_with_lower_inclusive_boundaries(
    data: st.DataObject, value: int
) -> None:
    inclusive_maximum = data.draw(st.integers(max_value=value))
    inclusive_minimum = data.draw(st.integers(max_value=inclusive_maximum))

    assume(inclusive_maximum != value)
    assume(inclusive_minimum != inclusive_maximum)

    template = ranges_between(minimum=inclusive_minimum, maximum=inclusive_maximum)

    assert template != value


@given(data=st.data(), value=st_value())
def test_constraint_returns_false_with_upper_inclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st.integers(min_value=value))
    exclusive_maximum = data.draw(st.integers(min_value=inclusive_minimum))

    assume(inclusive_minimum != value)
    assume(inclusive_minimum < exclusive_maximum - 1)

    template = ranges_between(minimum=inclusive_minimum, exclusive_maximum=exclusive_maximum)

    assert template != value


@given(data=st.data(), value=st_value())
def test_constraint_returns_false_with_lower_inclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    exclusive_maximum = data.draw(st.integers(max_value=value))
    inclusive_minimum = data.draw(st.integers(max_value=exclusive_maximum))

    assume(exclusive_maximum != value)
    assume(inclusive_minimum < exclusive_maximum - 1)

    template = ranges_between(minimum=inclusive_minimum, exclusive_maximum=exclusive_maximum)

    assert template != value


@given(data=st.data(), value=st_value())
def test_constraint_returns_false_with_upper_exclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    exclusive_minimum = data.draw(st.integers(min_value=value))
    inclusive_maximum = data.draw(st.integers(min_value=exclusive_minimum))

    assume(exclusive_minimum + 1 < inclusive_maximum)

    template = ranges_between(exclusive_minimum=exclusive_minimum, maximum=inclusive_maximum)

    assert template != value


@given(data=st.data(), value=st_value())
def test_constraint_returns_false_with_lower_exclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, value: int
) -> None:
    inclusive_maximum = data.draw(st.integers(max_value=value))
    exclusive_minimum = data.draw(st.integers(max_value=inclusive_maximum))

    assume(inclusive_maximum != value)
    assume(exclusive_minimum + 1 < inclusive_maximum)

    template = ranges_between(exclusive_minimum=exclusive_minimum, maximum=inclusive_maximum)

    assert template != value


@given(data=st.data(), value=st_value())
def test_constraint_returns_false_with_upper_exclusive_minimum_and_maximum(
    data: st.DataObject, value: int
) -> None:
    exclusive_minimum = data.draw(st.integers(min_value=value))
    exclusive_maximum = data.draw(st.integers(min_value=exclusive_minimum))

    assume(exclusive_minimum + 1 < exclusive_maximum - 1)

    template = ranges_between(
        exclusive_minimum=exclusive_minimum, exclusive_maximum=exclusive_maximum
    )

    assert template != value


@given(data=st.data(), value=st_value())
def test_constraint_returns_false_with_lower_exclusive_minimum_and_maximum(
    data: st.DataObject, value: int
) -> None:
    exclusive_maximum = data.draw(st.integers(max_value=value))
    exclusive_minimum = data.draw(st.integers(max_value=exclusive_maximum))

    assume(exclusive_minimum + 1 < exclusive_maximum - 1)

    template = ranges_between(
        exclusive_minimum=exclusive_minimum, exclusive_maximum=exclusive_maximum
    )

    assert template != value


def test_constraint_raises_type_error_on_missing_boundaries() -> None:
    template_partial = partial(ranges_between)

    with pytest.raises(TypeError):
        template_partial()


@given(data=st.data(), value=st_value())
def test_constraint_raises_value_error_on_missing_minimum_boundary(
    data: st.DataObject, value: int
) -> None:
    inclusive_maximum = data.draw(st_inclusive_maximum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    for boundary in [dict(maximum=inclusive_maximum), dict(exclusive_maximum=exclusive_maximum)]:
        template_partial = partial(ranges_between, **boundary)

        with pytest.raises(ValueError):
            template_partial()

        with pytest.raises(MissingBoundaryError):
            template_partial()


@given(data=st.data(), value=st_value())
def test_constraint_raises_value_error_on_missing_maximum_boundary(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    exclusive_minimum = data.draw(st_exclusive_minimum(value))

    for boundary in [dict(minimum=inclusive_minimum), dict(exclusive_minimum=exclusive_minimum)]:
        template_partial = partial(ranges_between, **boundary)

        with pytest.raises(ValueError):
            template_partial()

        with pytest.raises(MissingBoundaryError):
            template_partial()


@given(data=st.data(), value=st_value())
def test_constraint_raises_value_error_on_mutually_exclusive_minimum_boundaries(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    for maximum in [dict(maximum=inclusive_maximum), dict(exclusive_maximum=exclusive_maximum)]:
        template_partial = partial(
            ranges_between,
            minimum=inclusive_minimum,
            exclusive_minimum=exclusive_minimum,
            **maximum,
        )

        with pytest.raises(ValueError):
            template_partial()

        with pytest.raises(MutuallyExclusiveBoundariesError):
            template_partial()


@given(data=st.data(), value=st_value())
def test_constraint_raises_value_error_on_mutually_exclusive_maximum_boundaries(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    for minimum in [dict(minimum=inclusive_minimum), dict(exclusive_minimum=exclusive_minimum)]:
        template_partial = partial(
            ranges_between,
            maximum=inclusive_maximum,
            exclusive_maximum=exclusive_maximum,
            **minimum,
        )

        with pytest.raises(ValueError):
            template_partial()

        with pytest.raises(MutuallyExclusiveBoundariesError):
            template_partial()


@given(data=st.data(), value=st_value())
def test_constraint_raises_value_error_on_inclusive_boundaries_overlapping(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st_value())
    inclusive_maximum = data.draw(st_value(max_value=inclusive_minimum))

    assume(inclusive_minimum != inclusive_maximum)

    template_partial = partial(
        ranges_between, minimum=inclusive_minimum, maximum=inclusive_maximum
    )

    with pytest.raises(ValueError):
        template_partial()

    with pytest.raises(OverlappingBoundariesError):
        template_partial()


@given(data=st.data(), value=st_value())
def test_constraint_raises_value_error_on_inclusive_minimum_and_exclusive_maximum_overlapping(
    value: int
) -> None:
    raise NotImplementedError()


@given(data=st.data(), value=st_value())
def test_constraint_raises_value_error_on_exclusive_minimum_and_inclusive_maximum_overlapping(
    value: int
) -> None:
    raise NotImplementedError()


@given(data=st.data(), value=st_value())
def test_constraint_raises_value_error_on_exclusive_boundaries_overlapping(value: int) -> None:
    raise NotImplementedError()


@given(value=st_value())
def test_constraint_raises_value_error_on_single_match_with_inclusive_boundaries(
    value: int
) -> None:
    inclusive_minimum = value
    inclusive_maximum = value

    template_partial = partial(
        ranges_between, minimum=inclusive_minimum, maximum=inclusive_maximum
    )

    with pytest.raises(ValueError):
        template_partial()

    with pytest.raises(SingleMatchBoundariesError):
        template_partial()


@given(value=st_value())
def test_constraint_raises_value_error_on_single_match_with_inclusive_minimum_and_exclusive_maximum(
    value: int
) -> None:
    inclusive_minimum = value
    exclusive_maximum = value + 1

    template_partial = partial(
        ranges_between, minimum=inclusive_minimum, exclusive_maximum=exclusive_maximum
    )

    with pytest.raises(ValueError):
        template_partial()

    with pytest.raises(SingleMatchBoundariesError):
        template_partial()


@given(value=st_value())
def test_constraint_raises_value_error_on_single_match_with_exclusive_minimum_and_inclusive_maximum(
    value: int
) -> None:
    exclusive_minimum = value - 1
    inclusive_maximum = value

    template_partial = partial(
        ranges_between, exclusive_minimum=exclusive_minimum, maximum=inclusive_maximum
    )

    with pytest.raises(ValueError):
        template_partial()

    with pytest.raises(SingleMatchBoundariesError):
        template_partial()


@given(value=st_value())
def test_constraint_raises_value_error_on_single_match_with_exclusive_boundaries(
    value: int
) -> None:
    exclusive_minimum = value - 1
    exclusive_maximum = value + 1

    template_partial = partial(
        ranges_between, exclusive_minimum=exclusive_minimum, exclusive_maximum=exclusive_maximum
    )

    with pytest.raises(ValueError):
        template_partial()

    with pytest.raises(SingleMatchBoundariesError):
        template_partial()
