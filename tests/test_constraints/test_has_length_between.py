import sys

from typing import Sized, Literal, Final
from dataclasses import dataclass

import pytest

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import UNLIMITED
from testplates import (
    has_length_between,
    InvalidSignatureError,
    MissingBoundaryError,
    InvalidLengthError,
    OverlappingBoundariesError,
    SingleMatchBoundariesError,
)

from tests.conftest import Draw

MINIMUM_EXTREMUM: Final[Literal["minimum"]] = "minimum"
MAXIMUM_EXTREMUM: Final[Literal["maximum"]] = "maximum"

MINIMUM_ALLOWED_LENGTH: Final[int] = 0
MAXIMUM_ALLOWED_LENGTH: Final[int] = sys.maxsize


class NotSized:

    __len__ = None


@dataclass
class SizedWrapper(Sized):

    length: int

    def __len__(self) -> int:
        return self.length


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
@given(data=st.data(), length=st_length())
def test_repr_with_minimum_and_maximum(data: st.DataObject, length: int) -> None:
    fmt = "testplates.HasLengthBetween(minimum={minimum}, maximum={maximum})"

    minimum = data.draw(st_minimum(length))
    maximum = data.draw(st_maximum(length))

    assume(minimum != maximum)

    constraint = has_length_between(minimum=minimum, maximum=maximum)

    assert repr(constraint) == fmt.format(minimum=minimum, maximum=maximum)


@given(length=st_length())
def test_success_with_unlimited_minimum_and_unlimited_maximum(length: int) -> None:
    constraint = has_length_between(minimum=UNLIMITED, maximum=UNLIMITED)

    assert constraint == SizedWrapper(length)


# noinspection PyTypeChecker
@given(data=st.data(), length=st_length())
def test_success_with_minimum_and_maximum(data: st.DataObject, length: int) -> None:
    minimum = data.draw(st_minimum(length))
    maximum = data.draw(st_maximum(length))

    assume(minimum != maximum)

    constraint = has_length_between(minimum=minimum, maximum=maximum)

    assert constraint == SizedWrapper(length)


# noinspection PyTypeChecker
@given(data=st.data(), length=st_length())
def test_failure_when_value_is_above_minimum_and_maximum(data: st.DataObject, length: int) -> None:
    minimum = data.draw(st_length(min_value=length))
    maximum = data.draw(st_length(min_value=minimum))

    assume(minimum != length)
    assume(minimum != maximum)

    constraint = has_length_between(minimum=minimum, maximum=maximum)

    assert constraint != SizedWrapper(length)


# noinspection PyTypeChecker
@given(data=st.data(), length=st_length())
def test_failure_when_value_is_below_minimum_and_maximum(data: st.DataObject, length: int) -> None:
    maximum = data.draw(st_length(max_value=length))
    minimum = data.draw(st_length(max_value=maximum))

    assume(maximum != length)
    assume(minimum != maximum)

    constraint = has_length_between(minimum=minimum, maximum=maximum)

    assert constraint != SizedWrapper(length)


# noinspection PyTypeChecker
@given(data=st.data(), length=st_length())
def test_failure_when_value_is_not_sized(data: st.DataObject, length: int) -> None:
    minimum = data.draw(st_minimum(length))
    maximum = data.draw(st_maximum(length))

    assume(minimum != maximum)

    constraint = has_length_between(minimum=minimum, maximum=maximum)

    assert constraint != NotSized()


def test_failure_when_boundaries_are_missing() -> None:
    with pytest.raises(InvalidSignatureError):
        has_length_between()


# noinspection PyTypeChecker
@given(data=st.data(), length=st_length())
def test_failure_when_minimum_boundary_is_missing(data: st.DataObject, length: int) -> None:
    maximum = data.draw(st_maximum(length))

    with pytest.raises(MissingBoundaryError) as exception:
        has_length_between(maximum=maximum)

    assert exception.value.name == MINIMUM_EXTREMUM


# noinspection PyTypeChecker
@given(data=st.data(), length=st_length())
def test_failure_when_maximum_boundary_is_missing(data: st.DataObject, length: int) -> None:
    minimum = data.draw(st_minimum(length))

    with pytest.raises(MissingBoundaryError) as exception:
        has_length_between(minimum=minimum)

    assert exception.value.name == MAXIMUM_EXTREMUM


# noinspection PyTypeChecker
@given(data=st.data(), length=st_length())
def test_failure_when_boundaries_are_below_zero(data: st.DataObject, length: int) -> None:
    below_minimum = data.draw(st_length_below_minimum())

    with pytest.raises(InvalidLengthError) as exception:
        has_length_between(minimum=below_minimum, maximum=length)

    assert exception.value.boundary.value == below_minimum
    assert exception.value.boundary.is_inclusive is True

    with pytest.raises(InvalidLengthError) as exception:
        has_length_between(minimum=length, maximum=below_minimum)

    assert exception.value.boundary.value == below_minimum
    assert exception.value.boundary.is_inclusive is True


# noinspection PyTypeChecker
@given(data=st.data(), length=st_length())
def test_failure_when_boundaries_are_above_max_size(data: st.DataObject, length: int) -> None:
    above_maximum = data.draw(st_length_above_maximum())

    with pytest.raises(InvalidLengthError) as exception:
        has_length_between(minimum=above_maximum, maximum=length)

    assert exception.value.boundary.value == above_maximum
    assert exception.value.boundary.is_inclusive is True

    with pytest.raises(InvalidLengthError) as exception:
        has_length_between(minimum=length, maximum=above_maximum)

    assert exception.value.boundary.value == above_maximum
    assert exception.value.boundary.is_inclusive is True


# noinspection PyTypeChecker
@given(data=st.data())
def test_failure_when_boundaries_are_overlapping(data: st.DataObject) -> None:
    minimum = data.draw(st_length())
    maximum = data.draw(st_length(max_value=minimum))

    assume(minimum != maximum)

    with pytest.raises(OverlappingBoundariesError) as exception:
        has_length_between(minimum=minimum, maximum=maximum)

    assert exception.value.minimum.value == minimum
    assert exception.value.minimum.is_inclusive is True

    assert exception.value.maximum.value == maximum
    assert exception.value.maximum.is_inclusive is True


@given(length=st_length())
def test_failure_when_boundaries_match_single_value(length: int) -> None:
    with pytest.raises(SingleMatchBoundariesError) as exception:
        has_length_between(minimum=length, maximum=length)

    assert exception.value.minimum.value == length
    assert exception.value.minimum.is_inclusive is True

    assert exception.value.maximum.value == length
    assert exception.value.maximum.is_inclusive is True
