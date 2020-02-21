from typing import TypeVar, Generic, List
from dataclasses import dataclass

import pytest

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import contains, NotEnoughValuesError

from .conftest import st_anything, samples, Draw

_T = TypeVar("_T")


@dataclass
class Container(Generic[_T]):

    values: List[_T]

    def __contains__(self, item: _T) -> bool:
        return item in self.values


class NotContainer:

    __contains__ = None


@st.composite
def st_values(draw: Draw) -> List[_T]:
    return draw(st.lists(st_anything(), min_size=1))


@st.composite
def st_values_without(draw: Draw, value: _T) -> List[_T]:
    values = draw(st.lists(st_anything()))
    assume(value not in values)

    return values


@given(values=st_values())
def test_contains_returns_true(values: List[_T]) -> None:
    assert contains(*values) == Container(values)


@given(data=st.data(), value=st_anything())
def test_contains_returns_false(data: st.DataObject, value: _T) -> None:
    values = data.draw(st_values_without(value))

    assert contains(value, *samples(values)) != Container(values)


@given(values=st_values())
def test_contains_always_returns_false_when_value_is_not_a_container(values: List[_T]) -> None:
    assert contains(*values) != NotContainer()


def test_contains_raises_value_error_when_no_values_were_provided() -> None:
    with pytest.raises(ValueError):
        contains()

    with pytest.raises(NotEnoughValuesError):
        contains()
