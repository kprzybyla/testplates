import sys

from typing import (
    Sized,
    Literal,
    Final,
)

from dataclasses import dataclass

from resultful import (
    unwrap_success,
    unwrap_failure,
)

from hypothesis import (
    assume,
    given,
    strategies as st,
)

from testplates import (
    has_size_between,
    UNLIMITED,
    InvalidSizeError,
    UnlimitedRangeError,
    OverlappingBoundariesError,
    SingleMatchBoundariesError,
)

from tests.strategies import Draw

MINIMUM_EXTREMUM: Final[Literal["minimum"]] = "minimum"
MAXIMUM_EXTREMUM: Final[Literal["maximum"]] = "maximum"

MINIMUM_ALLOWED_SIZE: Final[int] = 0
MAXIMUM_ALLOWED_SIZE: Final[int] = sys.maxsize


class NotSized:

    __len__ = None


@dataclass
class SizedWrapper(Sized):

    size: int

    def __len__(self) -> int:
        return self.size


@st.composite
def st_size(
    draw: Draw[int],
    min_value: int = MINIMUM_ALLOWED_SIZE,
    max_value: int = MAXIMUM_ALLOWED_SIZE,
) -> int:
    return draw(st.integers(min_value=min_value, max_value=max_value))


@st.composite
def st_minimum(draw: Draw[int], size: int) -> int:
    return draw(st.integers(min_value=MINIMUM_ALLOWED_SIZE, max_value=size))


@st.composite
def st_maximum(draw: Draw[int], size: int) -> int:
    return draw(st.integers(min_value=size, max_value=MAXIMUM_ALLOWED_SIZE))


@st.composite
def st_size_below_minimum(draw: Draw[int]) -> int:
    below_minimum = draw(st.integers(max_value=MINIMUM_ALLOWED_SIZE))
    assume(below_minimum != MINIMUM_ALLOWED_SIZE)

    return below_minimum


@st.composite
def st_size_above_maximum(draw: Draw[int]) -> int:
    above_maximum = draw(st.integers(min_value=MAXIMUM_ALLOWED_SIZE))
    assume(above_maximum != MAXIMUM_ALLOWED_SIZE)

    return above_maximum


# noinspection PyTypeChecker
@given(data=st.data(), size=st_size())
def test_repr_with_minimum_and_maximum(data: st.DataObject, size: int) -> None:
    fmt = "testplates.has_size_between(minimum={minimum}, maximum={maximum})"

    minimum = data.draw(st_minimum(size))
    maximum = data.draw(st_maximum(size))

    assume(minimum != maximum)

    assert (result := has_size_between(minimum=minimum, maximum=maximum))

    constraint = unwrap_success(result)
    assert repr(constraint) == fmt.format(minimum=minimum, maximum=maximum)


# noinspection PyTypeChecker
@given(data=st.data(), size=st_size())
def test_success_with_minimum(data: st.DataObject, size: int) -> None:
    minimum = data.draw(st_minimum(size))

    assert (result := has_size_between(minimum=minimum, maximum=UNLIMITED))

    constraint = unwrap_success(result)
    assert constraint == SizedWrapper(size)


# noinspection PyTypeChecker
@given(data=st.data(), size=st_size())
def test_success_with_maximum(data: st.DataObject, size: int) -> None:
    maximum = data.draw(st_maximum(size))

    assert (result := has_size_between(minimum=UNLIMITED, maximum=maximum))

    constraint = unwrap_success(result)
    assert constraint == SizedWrapper(size)


# noinspection PyTypeChecker
@given(data=st.data(), size=st_size())
def test_success_with_minimum_and_maximum(data: st.DataObject, size: int) -> None:
    minimum = data.draw(st_minimum(size))
    maximum = data.draw(st_maximum(size))

    assume(minimum != maximum)

    assert (result := has_size_between(minimum=minimum, maximum=maximum))

    constraint = unwrap_success(result)
    assert constraint == SizedWrapper(size)


def test_failure_when_minimum_and_maximum_are_unlimited() -> None:
    assert not (result := has_size_between(minimum=UNLIMITED, maximum=UNLIMITED))

    error = unwrap_failure(result)
    assert isinstance(error, UnlimitedRangeError)


# noinspection PyTypeChecker
@given(data=st.data(), size=st_size())
def test_failure_when_value_is_above_minimum_and_maximum(data: st.DataObject, size: int) -> None:
    minimum = data.draw(st_size(min_value=size))
    maximum = data.draw(st_size(min_value=minimum))

    assume(minimum != size)
    assume(minimum != maximum)

    assert (result := has_size_between(minimum=minimum, maximum=maximum))

    constraint = unwrap_success(result)
    assert constraint != SizedWrapper(size)


# noinspection PyTypeChecker
@given(data=st.data(), size=st_size())
def test_failure_when_value_is_below_minimum_and_maximum(data: st.DataObject, size: int) -> None:
    maximum = data.draw(st_size(max_value=size))
    minimum = data.draw(st_size(max_value=maximum))

    assume(maximum != size)
    assume(minimum != maximum)

    assert (result := has_size_between(minimum=minimum, maximum=maximum))

    constraint = unwrap_success(result)
    assert constraint != SizedWrapper(size)


# noinspection PyTypeChecker
@given(data=st.data(), size=st_size())
def test_failure_when_value_is_not_sized(data: st.DataObject, size: int) -> None:
    minimum = data.draw(st_minimum(size))
    maximum = data.draw(st_maximum(size))

    assume(minimum != maximum)

    assert (result := has_size_between(minimum=minimum, maximum=maximum))

    constraint = unwrap_success(result)
    assert constraint != NotSized()


# noinspection PyTypeChecker
@given(data=st.data(), size=st_size())
def test_failure_when_boundaries_are_below_zero(data: st.DataObject, size: int) -> None:
    below_minimum = data.draw(st_size_below_minimum())

    assert not (result := has_size_between(minimum=below_minimum, maximum=size))

    error = unwrap_failure(result)
    assert isinstance(error, InvalidSizeError)
    assert error.boundary.value == below_minimum
    assert error.boundary.is_inclusive is True

    assert not (result := has_size_between(minimum=size, maximum=below_minimum))

    error = unwrap_failure(result)
    assert isinstance(error, InvalidSizeError)
    assert error.boundary.value == below_minimum
    assert error.boundary.is_inclusive is True


# noinspection PyTypeChecker
@given(data=st.data(), size=st_size())
def test_failure_when_boundaries_are_above_max_size(data: st.DataObject, size: int) -> None:
    above_maximum = data.draw(st_size_above_maximum())

    assert not (result := has_size_between(minimum=above_maximum, maximum=size))

    error = unwrap_failure(result)
    assert isinstance(error, InvalidSizeError)
    assert error.boundary.value == above_maximum
    assert error.boundary.is_inclusive is True

    assert not (result := has_size_between(minimum=size, maximum=above_maximum))

    error = unwrap_failure(result)
    assert isinstance(error, InvalidSizeError)
    assert error.boundary.value == above_maximum
    assert error.boundary.is_inclusive is True


# noinspection PyTypeChecker
@given(data=st.data())
def test_failure_when_boundaries_are_overlapping(data: st.DataObject) -> None:
    minimum = data.draw(st_size())
    maximum = data.draw(st_size(max_value=minimum))

    assume(minimum != maximum)

    assert not (result := has_size_between(minimum=minimum, maximum=maximum))

    error = unwrap_failure(result)
    assert isinstance(error, OverlappingBoundariesError)
    assert error.minimum.value == minimum
    assert error.minimum.is_inclusive is True
    assert error.maximum.value == maximum
    assert error.maximum.is_inclusive is True


# noinspection PyTypeChecker
@given(size=st_size())
def test_failure_when_boundaries_match_single_value(size: int) -> None:
    assert not (result := has_size_between(minimum=size, maximum=size))

    error = unwrap_failure(result)
    assert isinstance(error, SingleMatchBoundariesError)
    assert error.minimum.value == size
    assert error.minimum.is_inclusive is True
    assert error.maximum.value == size
    assert error.maximum.is_inclusive is True
