import sys

from dataclasses import dataclass
from typing import Sized, Final

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import has_length

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
def test_repr(length: int) -> None:
    fmt = "testplates.has_length({length})"

    constraint = has_length(length)

    assert repr(constraint) == fmt.format(length=length)


@given(data=st.data(), length=st_length())
def test_repr_with_minimum_and_maximum(data: st.DataObject, length: int) -> None:
    fmt = "testplates.has_length(minimum={minimum}, maximum={maximum})"

    minimum = data.draw(st_minimum(length))
    maximum = data.draw(st_maximum(length))

    assume(minimum != maximum)

    constraint = has_length(minimum=minimum, maximum=maximum)

    assert repr(constraint) == fmt.format(minimum=minimum, maximum=maximum)


@given(length=st_length())
def test_returns_true(length: int) -> None:
    constraint = has_length(length)

    assert constraint == SizedWrapper(length)


@given(data=st.data(), length=st_length())
def test_returns_true_with_minimum_and_maximum(data: st.DataObject, length: int) -> None:
    minimum = data.draw(st_minimum(length))
    maximum = data.draw(st_maximum(length))

    assume(minimum != maximum)

    constraint = has_length(minimum=minimum, maximum=maximum)

    assert constraint == SizedWrapper(length)


@given(length=st_length(), other=st_length())
def test_returns_false(length: int, other: int) -> None:
    assume(length != other)

    constraint = has_length(length)

    assert constraint != SizedWrapper(other)


@given(data=st.data(), length=st_length())
def test_returns_false_with_upper_minimum_and_maximum(data: st.DataObject, length: int) -> None:
    minimum = data.draw(st_length(min_value=length))
    maximum = data.draw(st_length(min_value=minimum))

    assume(minimum != length)
    assume(minimum != maximum)

    constraint = has_length(minimum=minimum, maximum=maximum)

    assert constraint != SizedWrapper(length)


@given(data=st.data(), length=st_length())
def test_returns_false_with_lower_minimum_and_maximum(data: st.DataObject, length: int) -> None:
    maximum = data.draw(st_length(max_value=length))
    minimum = data.draw(st_length(max_value=maximum))

    assume(maximum != length)
    assume(minimum != maximum)

    constraint = has_length(minimum=minimum, maximum=maximum)

    assert constraint != SizedWrapper(length)


@given(length=st_length())
def test_returns_false_when_value_is_not_sized(length: int) -> None:
    constraint = has_length(length)

    assert constraint != NotSized()


@given(data=st.data(), length=st_length())
def test_returns_false_when_value_is_not_sized_with_minimum_and_maximum(
    data: st.DataObject, length: int
) -> None:
    minimum = data.draw(st_minimum(length))
    maximum = data.draw(st_maximum(length))

    assume(minimum != maximum)

    constraint = has_length(minimum=minimum, maximum=maximum)

    assert constraint != NotSized()
