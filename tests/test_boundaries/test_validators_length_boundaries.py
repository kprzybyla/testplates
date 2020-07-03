import sys

from typing import Sized, Final
from dataclasses import dataclass

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import Success, Failure
from testplates.boundaries import (
    get_length_boundaries,
    fits_minimum_length,
    fits_maximum_length,
    UNLIMITED,
)

from testplates.exceptions import (
    MissingBoundaryError,
    InvalidLengthError,
    OverlappingBoundariesError,
    SingleMatchBoundariesError,
)

from tests.conftest import Draw

MINIMUM_ALLOWED_LENGTH: Final[int] = 0
MAXIMUM_ALLOWED_LENGTH: Final[int] = sys.maxsize


@dataclass
class SizedWrapper(Sized):

    length: int

    def __len__(self) -> int:
        return self.length


class NotSized:

    __len__ = None


@st.composite
def st_length(
    draw: Draw[int],
    min_value: int = MINIMUM_ALLOWED_LENGTH,
    max_value: int = MAXIMUM_ALLOWED_LENGTH,
) -> int:
    return draw(st.integers(min_value=min_value, max_value=max_value))


@st.composite
def st_minimum(draw: Draw[int], length: int) -> int:
    return draw(st.integers(min_value=MINIMUM_ALLOWED_LENGTH, max_value=length))


@st.composite
def st_maximum(draw: Draw[int], length: int) -> int:
    return draw(st.integers(min_value=length, max_value=MAXIMUM_ALLOWED_LENGTH))


@st.composite
def st_length_below_minimum(draw: Draw[int]) -> int:
    below_minimum = draw(st.integers(max_value=MINIMUM_ALLOWED_LENGTH))
    assume(below_minimum != MINIMUM_ALLOWED_LENGTH)

    return below_minimum


@st.composite
def st_length_above_maximum(draw: Draw[int]) -> int:
    above_maximum = draw(st.integers(min_value=MAXIMUM_ALLOWED_LENGTH))
    assume(above_maximum != MAXIMUM_ALLOWED_LENGTH)

    return above_maximum


# noinspection PyTypeChecker
@given(length=st_length())
def test_success_with_unlimited_minimum_and_unlimited_maximum(length: int) -> None:
    result = get_length_boundaries(inclusive_minimum=UNLIMITED, inclusive_maximum=UNLIMITED)

    minimum_boundary, maximum_boundary = Success.from_result(result).value

    assert fits_minimum_length(SizedWrapper(length), minimum_boundary)
    assert fits_maximum_length(SizedWrapper(length), maximum_boundary)


# noinspection PyTypeChecker
@given(data=st.data(), length=st_length())
def test_success_with_minimum_and_maximum(data: st.DataObject, length: int) -> None:
    minimum = data.draw(st_minimum(length))
    maximum = data.draw(st_maximum(length))

    assume(minimum != maximum)

    result = get_length_boundaries(inclusive_minimum=minimum, inclusive_maximum=maximum)

    minimum_boundary, maximum_boundary = Success.from_result(result).value

    assert fits_minimum_length(SizedWrapper(length), minimum_boundary)
    assert fits_maximum_length(SizedWrapper(length), maximum_boundary)


# noinspection PyTypeChecker
@given(data=st.data(), length=st_length())
def test_failure_when_value_is_above_minimum_and_maximum(data: st.DataObject, length: int) -> None:
    minimum = data.draw(st_length(min_value=length))
    maximum = data.draw(st_length(min_value=minimum))

    assume(minimum != length)
    assume(minimum != maximum)

    result = get_length_boundaries(inclusive_minimum=minimum, inclusive_maximum=maximum)

    minimum_boundary, maximum_boundary = Success.from_result(result).value

    assert not fits_minimum_length(SizedWrapper(length), minimum_boundary)
    assert fits_maximum_length(SizedWrapper(length), maximum_boundary)


# noinspection PyTypeChecker
@given(data=st.data(), length=st_length())
def test_failure_when_value_is_below_minimum_and_maximum(data: st.DataObject, length: int) -> None:
    maximum = data.draw(st_length(max_value=length))
    minimum = data.draw(st_length(max_value=maximum))

    assume(maximum != length)
    assume(minimum != maximum)

    result = get_length_boundaries(inclusive_minimum=minimum, inclusive_maximum=maximum)

    minimum_boundary, maximum_boundary = Success.from_result(result).value

    assert fits_minimum_length(SizedWrapper(length), minimum_boundary)
    assert not fits_maximum_length(SizedWrapper(length), maximum_boundary)


# noinspection PyTypeChecker
@given(data=st.data(), length=st_length())
def test_failure_when_value_is_not_sized(data: st.DataObject, length: int) -> None:
    minimum = data.draw(st_minimum(length))
    maximum = data.draw(st_maximum(length))

    assume(minimum != maximum)

    result = get_length_boundaries(inclusive_minimum=minimum, inclusive_maximum=maximum)

    minimum_boundary, maximum_boundary = Success.from_result(result).value

    assert not fits_minimum_length(NotSized(), minimum_boundary)  # type: ignore
    assert not fits_maximum_length(NotSized(), maximum_boundary)  # type: ignore


# noinspection PyArgumentList
def test_failure_when_boundaries_are_missing() -> None:
    result = get_length_boundaries()

    error = Failure.from_result(result).error

    assert isinstance(error, TypeError)


# noinspection PyTypeChecker
# noinspection PyArgumentList
@given(data=st.data(), length=st_length())
def test_failure_when_minimum_boundary_is_missing(data: st.DataObject, length: int) -> None:
    maximum = data.draw(st_maximum(length))

    result = get_length_boundaries(inclusive_maximum=maximum)

    error = Failure.from_result(result).error

    assert isinstance(error, MissingBoundaryError)


# noinspection PyTypeChecker
# noinspection PyArgumentList
@given(data=st.data(), length=st_length())
def test_failure_when_maximum_boundary_is_missing(data: st.DataObject, length: int) -> None:
    minimum = data.draw(st_minimum(length))

    result = get_length_boundaries(inclusive_minimum=minimum)

    error = Failure.from_result(result).error

    assert isinstance(error, MissingBoundaryError)


# noinspection PyTypeChecker
@given(data=st.data(), length=st_length())
def test_failure_when_boundaries_are_below_zero(data: st.DataObject, length: int) -> None:
    below_minimum = data.draw(st_length_below_minimum())

    result = get_length_boundaries(inclusive_minimum=below_minimum, inclusive_maximum=length)

    error = Failure.from_result(result).error

    assert isinstance(error, InvalidLengthError)

    result = get_length_boundaries(inclusive_minimum=length, inclusive_maximum=below_minimum)

    error = Failure.from_result(result).error

    assert isinstance(error, InvalidLengthError)


# noinspection PyTypeChecker
@given(data=st.data(), length=st_length())
def test_failure_when_boundaries_are_above_max_size(data: st.DataObject, length: int) -> None:
    above_maximum = data.draw(st_length_above_maximum())

    result = get_length_boundaries(inclusive_minimum=above_maximum, inclusive_maximum=length)

    error = Failure.from_result(result).error

    assert isinstance(error, InvalidLengthError)

    result = get_length_boundaries(inclusive_minimum=length, inclusive_maximum=above_maximum)

    error = Failure.from_result(result).error

    assert isinstance(error, InvalidLengthError)


# noinspection PyTypeChecker
@given(data=st.data())
def test_failure_when_boundaries_are_overlapping(data: st.DataObject) -> None:
    minimum = data.draw(st_length())
    maximum = data.draw(st_length(max_value=minimum))

    assume(minimum != maximum)

    result = get_length_boundaries(inclusive_minimum=minimum, inclusive_maximum=maximum)

    error = Failure.from_result(result).error

    assert isinstance(error, OverlappingBoundariesError)


@given(length=st_length())
def test_failure_when_boundaries_match_single_value(length: int) -> None:
    result = get_length_boundaries(inclusive_minimum=length, inclusive_maximum=length)

    error = Failure.from_result(result).error

    assert isinstance(error, SingleMatchBoundariesError)
