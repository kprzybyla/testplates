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
    minimum = data.draw(st_inclusive_minimum(value))
    maximum = data.draw(st_inclusive_maximum(value))

    assume(minimum != maximum)

    template = ranges_between(minimum=minimum, maximum=maximum)

    assert template == value


@given(data=st.data(), value=st_value())
def test_constraint_returns_true_with_inclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, value: int
):
    minimum = data.draw(st_inclusive_minimum(value))
    maximum = data.draw(st_exclusive_maximum(value))

    assume(minimum < maximum - 1)

    template = ranges_between(minimum=minimum, exclusive_maximum=maximum)

    assert template == value


@given(data=st.data(), value=st_value())
def test_constraint_returns_true_with_exclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, value: int
):
    minimum = data.draw(st_exclusive_minimum(value))
    maximum = data.draw(st_inclusive_maximum(value))

    assume(minimum + 1 < maximum)

    template = ranges_between(exclusive_minimum=minimum, maximum=maximum)

    assert template == value


@given(data=st.data(), value=st_value())
def test_constraint_returns_true_with_exclusive_minimum_and_maximum(
    data: st.DataObject, value: int
):
    minimum = data.draw(st_exclusive_minimum(value))
    maximum = data.draw(st_exclusive_maximum(value))

    assume(minimum + 1 < maximum - 1)

    template = ranges_between(exclusive_minimum=minimum, exclusive_maximum=maximum)

    assert template == value


def test_constraint_returns_false():
    # TODO(kprzybyla): FIXME
    raise NotImplementedError()


def test_constraint_raises_type_error_on_missing_boundaries() -> None:
    template_partial = partial(ranges_between)

    with pytest.raises(TypeError):
        template_partial()


@given(data=st.data(), value=st_value())
def test_constraint_raises_value_error_on_missing_minimum_boundary(
    data: st.DataObject, value: int
) -> None:
    inclusive = data.draw(st_inclusive_maximum(value))
    exclusive = data.draw(st_exclusive_maximum(value))

    for boundary in [dict(maximum=inclusive), dict(exclusive_maximum=exclusive)]:
        template_partial = partial(ranges_between, **boundary)

        with pytest.raises(ValueError):
            template_partial()

        with pytest.raises(MissingBoundaryError):
            template_partial()


@given(data=st.data(), value=st_value())
def test_constraint_raises_value_error_on_missing_maximum_boundary(
    data: st.DataObject, value: int
) -> None:
    inclusive = data.draw(st_inclusive_minimum(value))
    exclusive = data.draw(st_exclusive_minimum(value))

    for boundary in [dict(minimum=inclusive), dict(exclusive_minimum=exclusive)]:
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
def test_constraint_raises_value_error_on_boundaries_overlapping(
    data: st.DataObject, value: int
) -> None:
    minimum = data.draw(st_value())
    maximum = data.draw(st_value(max_value=minimum))

    assume(minimum != maximum)

    template_partial = partial(ranges_between, minimum=minimum, maximum=maximum)

    with pytest.raises(ValueError):
        template_partial()

    with pytest.raises(OverlappingBoundariesError):
        template_partial()
