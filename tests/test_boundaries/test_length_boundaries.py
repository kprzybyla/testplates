import sys

from typing import Final

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates.boundaries import get_length_boundaries
from testplates.exceptions import (
    MissingBoundaryError,
    InvalidLengthError,
    OverlappingBoundariesError,
    SingleMatchBoundariesError,
)

from tests.conftest import Draw

MINIMUM_LENGTH: Final[int] = 0
MAXIMUM_LENGTH: Final[int] = sys.maxsize


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


# noinspection PyArgumentList
def test_raises_error_on_no_parameters() -> None:
    result = get_length_boundaries()  # type: ignore

    assert result.is_error
    assert isinstance(result.error, TypeError)


# noinspection PyTypeChecker
# noinspection PyArgumentList
@given(data=st.data(), length=st_length())
def test_raises_error_on_missing_minimum_boundary(data: st.DataObject, length: int) -> None:
    maximum = data.draw(st_maximum(length))

    result = get_length_boundaries(inclusive_maximum=maximum)  # type: ignore

    assert result.is_error
    assert isinstance(result.error, MissingBoundaryError)


# noinspection PyTypeChecker
# noinspection PyArgumentList
@given(data=st.data(), length=st_length())
def test_raises_error_on_missing_maximum_boundary(data: st.DataObject, length: int) -> None:
    minimum = data.draw(st_minimum(length))

    result = get_length_boundaries(inclusive_minimum=minimum)  # type: ignore

    assert result.is_error
    assert isinstance(result.error, MissingBoundaryError)


# noinspection PyTypeChecker
@given(data=st.data(), length=st_length())
def test_raises_error_on_boundaries_below_zero(data: st.DataObject, length: int) -> None:
    below_minimum = data.draw(st_length_below_minimum())

    assume(below_minimum != MINIMUM_LENGTH)

    result = get_length_boundaries(inclusive_minimum=below_minimum, inclusive_maximum=length)

    assert result.is_error
    assert isinstance(result.error, InvalidLengthError)

    result = get_length_boundaries(inclusive_minimum=length, inclusive_maximum=below_minimum)

    assert result.is_error
    assert isinstance(result.error, InvalidLengthError)


# noinspection PyTypeChecker
@given(data=st.data(), length=st_length())
def test_raises_error_on_boundaries_above_max_size(data: st.DataObject, length: int) -> None:
    above_maximum = data.draw(st_length_above_maximum())

    assume(above_maximum != MAXIMUM_LENGTH)

    result = get_length_boundaries(inclusive_minimum=above_maximum, inclusive_maximum=length)

    assert result.is_error
    assert isinstance(result.error, InvalidLengthError)

    result = get_length_boundaries(inclusive_minimum=length, inclusive_maximum=above_maximum)

    assert result.is_error
    assert isinstance(result.error, InvalidLengthError)


# noinspection PyTypeChecker
@given(data=st.data())
def test_raises_error_on_boundaries_overlapping(data: st.DataObject) -> None:
    minimum = data.draw(st_length())
    maximum = data.draw(st_length(max_value=minimum))

    assume(minimum != maximum)

    result = get_length_boundaries(inclusive_minimum=minimum, inclusive_maximum=maximum)

    assert result.is_error
    assert isinstance(result.error, OverlappingBoundariesError)


@given(length=st_length())
def test_raises_error_on_single_match_boundaries(length: int) -> None:
    result = get_length_boundaries(inclusive_minimum=length, inclusive_maximum=length)

    assert result.is_error
    assert isinstance(result.error, SingleMatchBoundariesError)
