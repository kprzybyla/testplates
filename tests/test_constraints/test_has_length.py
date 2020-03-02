import sys

from functools import partial
from dataclasses import dataclass

import pytest

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import (
    has_length,
    MissingBoundaryValueError,
    OverlappingBoundariesValueError,
    SingleMatchBoundariesValueError,
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
def st_length(draw: Draw) -> int:
    return draw(st.integers(min_value=0, max_value=sys.maxsize))


@st.composite
def st_minimum(draw: Draw, length: int) -> int:
    return draw(st.integers(min_value=0, max_value=length))


@st.composite
def st_maximum(draw: Draw, length: int) -> int:
    maximum = draw(st.integers(min_value=length, max_value=sys.maxsize))

    return maximum


@st.composite
def st_inverse_upper_minimum(draw: Draw, length: int) -> int:
    minimum = draw(st.integers(min_value=length, max_value=sys.maxsize))
    assume(minimum > length)

    return minimum


@st.composite
def st_inverse_upper_maximum(draw: Draw, minimum: int) -> int:
    maximum = draw(st.integers(min_value=minimum, max_value=sys.maxsize))
    assume(minimum != maximum)

    return maximum


@st.composite
def st_inverse_lower_minimum(draw: Draw, length: int) -> int:
    minimum = draw(st.integers(min_value=0, max_value=length))
    assume(minimum < length)

    return minimum


@st.composite
def st_inverse_lower_maximum(draw: Draw, length: int, minimum: int) -> int:
    maximum = draw(st.integers(min_value=minimum, max_value=length))
    assume(maximum < length)
    assume(minimum != maximum)

    return maximum


@given(length=st_length())
def test_has_length_returns_true(length: int) -> None:
    template = has_length(length)

    assert template == Sized(length)


@given(data=st.data(), length=st_length())
def test_has_length_with_range_returns_true(data: st.DataObject, length: int) -> None:
    minimum = data.draw(st_minimum(length))
    maximum = data.draw(st_maximum(length))

    assume(minimum != maximum)

    template = has_length(minimum=minimum, maximum=maximum)

    assert template == Sized(length)


@given(length=st_length(), other=st_length())
def test_has_length_returns_false(length: int, other: int) -> None:
    assume(length != other)

    template = has_length(length)

    assert template != Sized(other)


@given(data=st.data(), length=st_length())
def test_has_length_with_range_returns_false_on_length_under_range(
    data: st.DataObject, length: int
) -> None:
    minimum = data.draw(st_inverse_upper_minimum(length))
    maximum = data.draw(st_inverse_upper_maximum(minimum))

    template = has_length(minimum=minimum, maximum=maximum)

    assert template != Sized(length)


@given(data=st.data(), length=st_length())
def test_has_length_with_range_returns_false_on_length_above_range(
    data: st.DataObject, length: int
) -> None:
    minimum = data.draw(st_inverse_lower_minimum(length))
    maximum = data.draw(st_inverse_lower_maximum(length, minimum))

    template = has_length(minimum=minimum, maximum=maximum)

    assert template != Sized(length)


@given(length=st_length())
def test_has_length_always_returns_false_when_value_is_not_sized(length: int) -> None:
    template = has_length(length)

    assert template != NotSized()


@given(data=st.data(), length=st_length())
def test_has_length_with_range_always_returns_false_when_value_is_not_sized(
    data: st.DataObject, length: int
) -> None:
    minimum = data.draw(st_minimum(length))
    maximum = data.draw(st_maximum(length))

    assume(minimum != maximum)

    template = has_length(minimum=minimum, maximum=maximum)

    assert template != NotSized()


def test_has_length_raises_type_error_on_no_parameters() -> None:
    with pytest.raises(TypeError):
        has_length()


@given(data=st.data(), length=st_length())
def test_has_length_raises_value_error_on_missing_minimum_boundary(
    data: st.DataObject, length: int
) -> None:
    maximum = data.draw(st_maximum(length))

    has_length_partial = partial(has_length, maximum=maximum)

    with pytest.raises(ValueError):
        has_length_partial()

    with pytest.raises(MissingBoundaryValueError):
        has_length_partial()


@given(data=st.data(), length=st_length())
def test_has_length_raises_value_error_on_missing_maximum_boundary(
    data: st.DataObject, length: int
) -> None:
    minimum = data.draw(st_minimum(length))

    has_length_partial = partial(has_length, minimum=minimum)

    with pytest.raises(ValueError):
        has_length_partial()

    with pytest.raises(MissingBoundaryValueError):
        has_length_partial()


@given(data=st.data())
def test_has_length_raises_value_error_on_boundaries_overlapping(data: st.DataObject) -> None:
    minimum = data.draw(st_minimum(sys.maxsize))
    maximum = data.draw(st_minimum(minimum))

    assume(minimum != maximum)

    has_length_partial = partial(has_length, minimum=minimum, maximum=maximum)

    with pytest.raises(ValueError):
        has_length_partial()

    with pytest.raises(OverlappingBoundariesValueError):
        has_length_partial()


@given(length=st_length())
def test_has_length_raises_value_error_when_minimum_equals_to_maximum(length: int) -> None:
    has_length_partial = partial(has_length, minimum=length, maximum=length)

    with pytest.raises(ValueError):
        has_length_partial()

    with pytest.raises(SingleMatchBoundariesValueError):
        has_length_partial()
