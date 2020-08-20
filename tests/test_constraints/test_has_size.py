import sys

from dataclasses import dataclass
from typing import Sized, Final

from resultful import unwrap_success
from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import has_size

from tests.strategies import Draw

MINIMUM_ALLOWED_SIZE: Final[int] = 0
MAXIMUM_ALLOWED_SIZE: Final[int] = sys.maxsize


@dataclass
class SizedWrapper(Sized):

    size: int

    def __len__(self) -> int:
        return self.size


class NotSized:

    __len__ = None


@st.composite
def st_size(
    draw: Draw[int], min_value: int = MINIMUM_ALLOWED_SIZE, max_value: int = MAXIMUM_ALLOWED_SIZE
) -> int:
    return draw(st.integers(min_value=min_value, max_value=max_value))


# noinspection PyTypeChecker
@given(size=st_size())
def test_repr(size: int) -> None:
    fmt = "testplates.has_size({size})"

    assert (result := has_size(size))

    constraint = unwrap_success(result)
    assert repr(constraint) == fmt.format(size=size)


# noinspection PyTypeChecker
@given(size=st_size())
def test_returns_true(size: int) -> None:
    assert (result := has_size(size))

    constraint = unwrap_success(result)
    assert constraint == SizedWrapper(size)


# noinspection PyTypeChecker
@given(size=st_size(), other=st_size())
def test_returns_false(size: int, other: int) -> None:
    assume(size != other)

    assert (result := has_size(size))

    constraint = unwrap_success(result)
    assert constraint != SizedWrapper(other)


# noinspection PyTypeChecker
@given(size=st_size())
def test_returns_false_when_value_is_not_sized(size: int) -> None:
    assert (result := has_size(size))

    constraint = unwrap_success(result)
    assert constraint != NotSized()
