import sys

from dataclasses import dataclass
from typing import Sized, Final

import pytest

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import (
    has_length,
    MissingBoundaryError,
    InvalidLengthError,
    OverlappingBoundariesError,
    SingleMatchBoundariesError,
)

from tests.conftest import Draw

MINIMUM_LENGTH: Final[int] = 0
MAXIMUM_LENGTH: Final[int] = sys.maxsize


@dataclass
class SizedWrapper(Sized):

    length: int

    def __len__(self) -> int:
        return self.length


class NotSized:

    __len__ = None


@st.composite
def st_length(
    draw: Draw[int], min_value: int = MINIMUM_LENGTH, max_value: int = MAXIMUM_LENGTH
) -> int:
    return draw(st.integers(min_value=min_value, max_value=max_value))


@st.composite
def st_minimum(draw: Draw[int], length: int) -> int:
    return draw(st.integers(min_value=MINIMUM_LENGTH, max_value=length))


@st.composite
def st_maximum(draw: Draw[int], length: int) -> int:
    maximum = draw(st.integers(min_value=length, max_value=MAXIMUM_LENGTH))

    return maximum


@st.composite
def st_length_below_minimum(draw: Draw[int]) -> int:
    return draw(st.integers(max_value=MINIMUM_LENGTH))


@st.composite
def st_length_above_maximum(draw: Draw[int]) -> int:
    return draw(st.integers(min_value=MAXIMUM_LENGTH))


@given(length=st_length())
def test_returns_true(length: int) -> None:
    template = has_length(length)

    assert template == SizedWrapper(length)


@given(data=st.data(), length=st_length())
def test_returns_true_with_minimum_and_maximum(data: st.DataObject, length: int) -> None:
    minimum = data.draw(st_minimum(length))
    maximum = data.draw(st_maximum(length))

    assume(minimum != maximum)

    template = has_length(minimum=minimum, maximum=maximum)

    assert template == SizedWrapper(length)


@given(length=st_length(), other=st_length())
def test_returns_false(length: int, other: int) -> None:
    assume(length != other)

    template = has_length(length)

    assert template != SizedWrapper(other)


@given(data=st.data(), length=st_length())
def test_returns_false_with_upper_minimum_and_maximum(data: st.DataObject, length: int) -> None:
    minimum = data.draw(st_length(min_value=length))
    maximum = data.draw(st_length(min_value=minimum))

    assume(minimum != length)
    assume(minimum != maximum)

    template = has_length(minimum=minimum, maximum=maximum)

    assert template != SizedWrapper(length)


@given(data=st.data(), length=st_length())
def test_returns_false_with_lower_minimum_and_maximum(data: st.DataObject, length: int) -> None:
    maximum = data.draw(st_length(max_value=length))
    minimum = data.draw(st_length(max_value=maximum))

    assume(maximum != length)
    assume(minimum != maximum)

    template = has_length(minimum=minimum, maximum=maximum)

    assert template != SizedWrapper(length)


@given(length=st_length())
def test_returns_false_when_value_is_not_sized(length: int) -> None:
    template = has_length(length)

    assert template != NotSized()


@given(data=st.data(), length=st_length())
def test_returns_false_when_value_is_not_sized_with_minimum_and_maximum(
    data: st.DataObject, length: int
) -> None:
    minimum = data.draw(st_minimum(length))
    maximum = data.draw(st_maximum(length))

    assume(minimum != maximum)

    template = has_length(minimum=minimum, maximum=maximum)

    assert template != NotSized()


# noinspection PyArgumentList
def test_raises_error_on_no_parameters() -> None:
    with pytest.raises(TypeError):
        has_length()  # type: ignore


# noinspection PyArgumentList
@given(data=st.data(), length=st_length())
def test_raises_error_on_missing_minimum_boundary(data: st.DataObject, length: int) -> None:
    maximum = data.draw(st_maximum(length))

    with pytest.raises(MissingBoundaryError):
        has_length(maximum=maximum)  # type: ignore


# noinspection PyArgumentList
@given(data=st.data(), length=st_length())
def test_raises_error_on_missing_maximum_boundary(data: st.DataObject, length: int) -> None:
    minimum = data.draw(st_minimum(length))

    with pytest.raises(MissingBoundaryError):
        has_length(minimum=minimum)  # type: ignore


@given(data=st.data(), length=st_length())
def test_raises_error_on_boundaries_below_zero(data: st.DataObject, length: int) -> None:
    below_minimum = data.draw(st_length_below_minimum())

    assume(below_minimum != MINIMUM_LENGTH)

    with pytest.raises(InvalidLengthError):
        has_length(minimum=below_minimum, maximum=length)

    with pytest.raises(InvalidLengthError):
        has_length(minimum=length, maximum=below_minimum)


@given(data=st.data(), length=st_length())
def test_raises_error_on_boundaries_above_max_size(data: st.DataObject, length: int) -> None:
    above_maximum = data.draw(st_length_above_maximum())

    assume(above_maximum != MAXIMUM_LENGTH)

    with pytest.raises(InvalidLengthError):
        has_length(minimum=above_maximum, maximum=length)

    with pytest.raises(InvalidLengthError):
        has_length(minimum=length, maximum=above_maximum)


@given(data=st.data())
def test_raises_error_on_boundaries_overlapping(data: st.DataObject) -> None:
    minimum = data.draw(st_length())
    maximum = data.draw(st_length(max_value=minimum))

    assume(minimum != maximum)

    with pytest.raises(OverlappingBoundariesError):
        has_length(minimum=minimum, maximum=maximum)


@given(length=st_length())
def test_raises_error_on_single_match_boundaries(length: int) -> None:
    with pytest.raises(SingleMatchBoundariesError):
        has_length(minimum=length, maximum=length)
