import sys

from typing import (
    Sized,
    Final,
)

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
    has_minimum_size,
    InvalidSizeError,
)

from tests.strategies import Draw

MINIMUM_ALLOWED_SIZE: Final[int] = 0
MAXIMUM_ALLOWED_SIZE: Final[int] = sys.maxsize


class NotSized:

    __len__ = None


class SizedWrapper(Sized):

    __slots__ = ("size",)

    def __init__(self, size: int) -> None:
        self.size = size

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
def test_repr(data: st.DataObject, size: int) -> None:
    fmt = "testplates.has_minimum_size(minimum={minimum})"

    minimum = data.draw(st_minimum(size))

    assert (result := has_minimum_size(minimum))

    constraint = unwrap_success(result)
    assert repr(constraint) == fmt.format(minimum=minimum)


# noinspection PyTypeChecker
@given(data=st.data(), size=st_size())
def test_success(data: st.DataObject, size: int) -> None:
    minimum = data.draw(st_minimum(size))

    assert (result := has_minimum_size(minimum))

    constraint = unwrap_success(result)
    assert constraint == SizedWrapper(size)


# noinspection PyTypeChecker
@given(data=st.data(), size=st_size())
def test_failure_when_value_is_below_minimum(data: st.DataObject, size: int) -> None:
    minimum = data.draw(st_size(min_value=size))

    assume(minimum != size)

    assert (result := has_minimum_size(minimum))

    constraint = unwrap_success(result)
    assert constraint != SizedWrapper(size)


# noinspection PyTypeChecker
@given(data=st.data(), size=st_size())
def test_failure_when_value_is_not_sized(data: st.DataObject, size: int) -> None:
    minimum = data.draw(st_minimum(size))

    assert (result := has_minimum_size(minimum))

    constraint = unwrap_success(result)
    assert constraint != NotSized()


# noinspection PyTypeChecker
@given(data=st.data())
def test_failure_when_minimum_is_below_zero(data: st.DataObject) -> None:
    below_minimum = data.draw(st_size_below_minimum())

    assert not (result := has_minimum_size(below_minimum))

    error = unwrap_failure(result)
    assert isinstance(error, InvalidSizeError)
    assert error.boundary.value == below_minimum
    assert error.boundary.is_inclusive is True


# noinspection PyTypeChecker
@given(data=st.data())
def test_failure_when_minimum_is_above_max_size(data: st.DataObject) -> None:
    above_maximum = data.draw(st_size_above_maximum())

    assert not (result := has_minimum_size(above_maximum))

    error = unwrap_failure(result)
    assert isinstance(error, InvalidSizeError)
    assert error.boundary.value == above_maximum
    assert error.boundary.is_inclusive is True
