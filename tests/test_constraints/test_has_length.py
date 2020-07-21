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


@given(length=st_length())
def test_repr(length: int) -> None:
    fmt = "testplates.HasLength({length})"

    constraint = has_length(length)

    assert repr(constraint) == fmt.format(length=length)


@given(length=st_length())
def test_returns_true(length: int) -> None:
    constraint = has_length(length)

    assert constraint == SizedWrapper(length)


@given(length=st_length(), other=st_length())
def test_returns_false(length: int, other: int) -> None:
    assume(length != other)

    constraint = has_length(length)

    assert constraint != SizedWrapper(other)


@given(length=st_length())
def test_returns_false_when_value_is_not_sized(length: int) -> None:
    constraint = has_length(length)

    assert constraint != NotSized()
