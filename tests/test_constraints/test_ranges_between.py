from functools import partial

import pytest

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import (
    ranges_between,
    MissingBoundaryValueError,
    MutuallyExclusiveBoundaryValueError,
)

from ..conftest import Draw


@st.composite
def st_value(draw: Draw) -> int:
    return draw(st.integers())


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
def test_ranges_between_returns_true_with_exclusive_minimum_and_maximum(
    data: st.DataObject, value: int
):
    minimum = data.draw(st_exclusive_minimum(value))
    maximum = data.draw(st_exclusive_maximum(value))

    assume(minimum + 1 < maximum - 1)

    template = ranges_between(exclusive_minimum=minimum, exclusive_maximum=maximum)

    assert template == value


@given(data=st.data(), value=st_value())
def test_ranges_between_returns_true_with_inclusive_minimum_and_maximum(
    data: st.DataObject, value: int
):
    minimum = data.draw(st_inclusive_minimum(value))
    maximum = data.draw(st_inclusive_maximum(value))

    assume(minimum != maximum)

    template = ranges_between(minimum=minimum, maximum=maximum)

    assert template == value


@given(data=st.data(), value=st_value())
def test_ranges_between_returns_true_with_exclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, value: int
):
    minimum = data.draw(st_exclusive_minimum(value))
    maximum = data.draw(st_inclusive_maximum(value))

    assume(minimum + 1 < maximum)

    template = ranges_between(exclusive_minimum=minimum, maximum=maximum)

    assert template == value


@given(data=st.data(), value=st_value())
def test_ranges_between_returns_true_with_inclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, value: int
):
    minimum = data.draw(st_inclusive_minimum(value))
    maximum = data.draw(st_exclusive_maximum(value))

    assume(minimum < maximum - 1)

    template = ranges_between(minimum=minimum, exclusive_maximum=maximum)

    assert template == value


def test_ranges_between_returns_false():
    raise NotImplementedError()


def test_ranges_between_raises_type_error_on_missing_boundaries() -> None:
    ranges_between_partial = partial(ranges_between)

    with pytest.raises(TypeError):
        ranges_between_partial()


@given(data=st.data(), value=st_value())
def test_ranges_between_raises_value_error_on_missing_minimum_boundary(
    data: st.DataObject, value: int
) -> None:
    boundaries = [
        dict(maximum=data.draw(st_inclusive_maximum(value))),
        dict(exclusive_maximum=data.draw(st_exclusive_maximum(value))),
    ]

    for boundary in boundaries:
        ranges_between_partial = partial(ranges_between, **boundary)

        with pytest.raises(ValueError):
            ranges_between_partial()

        with pytest.raises(MissingBoundaryValueError):
            ranges_between_partial()


@given(data=st.data(), value=st_value())
def test_ranges_between_raises_value_error_on_missing_maximum_boundary(
    data: st.DataObject, value: int
) -> None:
    boundaries = [
        dict(minimum=data.draw(st_inclusive_minimum(value))),
        dict(exclusive_minimum=data.draw(st_exclusive_minimum(value))),
    ]

    for boundary in boundaries:
        ranges_between_partial = partial(ranges_between, **boundary)

        with pytest.raises(ValueError):
            ranges_between_partial()

        with pytest.raises(MissingBoundaryValueError):
            ranges_between_partial()


@given(data=st.data(), value=st_value())
def test_ranges_between_raises_value_error_on_mutually_exclusive_minimum_boundaries(
    data: st.DataObject, value: int
) -> None:
    maximums = [
        dict(maximum=data.draw(st_inclusive_maximum(value))),
        dict(exclusive_maximum=data.draw(st_exclusive_maximum(value))),
    ]

    for maximum in maximums:
        ranges_between_partial = partial(
            ranges_between,
            minimum=data.draw(st_inclusive_minimum(value)),
            exclusive_minimum=data.draw(st_exclusive_minimum(value)),
            **maximum,
        )

        with pytest.raises(ValueError):
            ranges_between_partial()

        with pytest.raises(MutuallyExclusiveBoundaryValueError):
            ranges_between_partial()


@given(data=st.data(), value=st_value())
def test_ranges_between_raises_value_error_on_mutually_exclusive_maximum_boundaries(
    data: st.DataObject, value: int
) -> None:
    minimums = [
        dict(minimum=data.draw(st_inclusive_minimum(value))),
        dict(exclusive_minimum=data.draw(st_exclusive_minimum(value))),
    ]

    for minimum in minimums:
        ranges_between_partial = partial(
            ranges_between,
            maximum=data.draw(st_inclusive_maximum(value)),
            exclusive_maximum=data.draw(st_exclusive_maximum(value)),
            **minimum,
        )

        with pytest.raises(ValueError):
            ranges_between_partial()

        with pytest.raises(MutuallyExclusiveBoundaryValueError):
            ranges_between_partial()


def test_ranges_between_raises_value_error_on_boundaries_overlapping():
    raise NotImplementedError()
