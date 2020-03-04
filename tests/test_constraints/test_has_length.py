import sys

from functools import partial
from dataclasses import dataclass

import pytest

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import (
    has_length,
    MissingBoundaryError,
    InvalidBoundaryValueError,
    OverlappingBoundariesError,
    SingleMatchBoundariesError,
)

from ..conftest import Draw


@dataclass
class Sized:

    length: int

    def __len__(self) -> int:
        return self.length


class NotSized:

    __len__ = None


@st.composite
def st_length(draw: Draw, max_value: int = sys.maxsize) -> int:
    return draw(st.integers(min_value=0, max_value=max_value))


@st.composite
def st_inverse_length(draw: Draw) -> int:
    length = draw(st.integers(max_value=0))
    assume(length != 0)

    return length


@st.composite
def st_minimum(draw: Draw, length: int) -> int:
    return draw(st.integers(min_value=0, max_value=length))


@st.composite
def st_maximum(draw: Draw, length: int) -> int:
    maximum = draw(st.integers(min_value=length, max_value=sys.maxsize))

    return maximum


@given(length=st_length())
def test_constraint_returns_true(length: int) -> None:
    template = has_length(length)

    assert template == Sized(length)


@given(data=st.data(), length=st_length())
def test_constraint_returns_true_with_range(data: st.DataObject, length: int) -> None:
    minimum = data.draw(st_minimum(length))
    maximum = data.draw(st_maximum(length))

    assume(minimum != maximum)

    template = has_length(minimum=minimum, maximum=maximum)

    assert template == Sized(length)


@given(length=st_length(), other=st_length())
def test_constraint_returns_false(length: int, other: int) -> None:
    assume(length != other)

    template = has_length(length)

    assert template != Sized(other)


@given(data=st.data(), length=st_length())
def test_constraint_returns_false_with_upper_range(data: st.DataObject, length: int) -> None:
    minimum = data.draw(st.integers(min_value=length, max_value=sys.maxsize))
    maximum = data.draw(st.integers(min_value=minimum, max_value=sys.maxsize))

    assume(minimum != length)
    assume(minimum != maximum)

    template = has_length(minimum=minimum, maximum=maximum)

    assert template != Sized(length)


@given(data=st.data(), length=st_length())
def test_constraint_returns_false_with_lower_range(data: st.DataObject, length: int) -> None:
    maximum = data.draw(st.integers(min_value=0, max_value=length))
    minimum = data.draw(st.integers(min_value=0, max_value=maximum))

    assume(maximum != length)
    assume(minimum != maximum)

    template = has_length(minimum=minimum, maximum=maximum)

    assert template != Sized(length)


@given(length=st_length())
def test_constraint_always_returns_false_when_value_is_not_sized(length: int) -> None:
    template = has_length(length)

    assert template != NotSized()


@given(data=st.data(), length=st_length())
def test_constraint_always_returns_false_when_value_is_not_sized_with_range(
    data: st.DataObject, length: int
) -> None:
    minimum = data.draw(st_minimum(length))
    maximum = data.draw(st_maximum(length))

    assume(minimum != maximum)

    template = has_length(minimum=minimum, maximum=maximum)

    assert template != NotSized()


def test_constraint_raises_type_error_on_no_parameters() -> None:
    template_partial = partial(has_length)

    with pytest.raises(TypeError):
        template_partial()


@given(data=st.data(), length=st_length())
def test_constraint_raises_value_error_on_missing_minimum_boundary(
    data: st.DataObject, length: int
) -> None:
    maximum = data.draw(st_maximum(length))

    template_partial = partial(has_length, maximum=maximum)

    with pytest.raises(ValueError):
        template_partial()

    with pytest.raises(MissingBoundaryError):
        template_partial()


@given(data=st.data(), length=st_length())
def test_constraint_raises_value_error_on_missing_maximum_boundary(
    data: st.DataObject, length: int
) -> None:
    minimum = data.draw(st_minimum(length))

    template_partial = partial(has_length, minimum=minimum)

    with pytest.raises(ValueError):
        template_partial()

    with pytest.raises(MissingBoundaryError):
        template_partial()


@given(length=st_inverse_length())
def test_constraint_raises_value_error_on_minimum_boundary_below_zero(length: int) -> None:
    template_partial = partial(has_length, minimum=length)

    with pytest.raises(ValueError):
        template_partial()

    with pytest.raises(InvalidBoundaryValueError):
        template_partial()


@given(length=st_inverse_length())
def test_constraint_raises_value_error_on_maximum_boundary_below_zero(length: int) -> None:
    template_partial = partial(has_length, maximum=length)

    with pytest.raises(ValueError):
        template_partial()

    with pytest.raises(InvalidBoundaryValueError):
        template_partial()


@given(data=st.data())
def test_constraint_raises_value_error_on_boundaries_overlapping(data: st.DataObject) -> None:
    minimum = data.draw(st_length())
    maximum = data.draw(st_length(max_value=minimum))

    assume(minimum != maximum)

    template_partial = partial(has_length, minimum=minimum, maximum=maximum)

    with pytest.raises(ValueError):
        template_partial()

    with pytest.raises(OverlappingBoundariesError):
        template_partial()


@given(length=st_length())
def test_constraint_raises_value_error_on_single_match_boundaries(length: int) -> None:
    template_partial = partial(has_length, minimum=length, maximum=length)

    with pytest.raises(ValueError):
        template_partial()

    with pytest.raises(SingleMatchBoundariesError):
        template_partial()
