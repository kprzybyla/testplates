from typing import TypeVar, Generic, List
from functools import partial
from dataclasses import dataclass

import pytest

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import contains, TooLittleValuesError

from ..conftest import st_anything, samples, Draw

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
def test_constraint_returns_true(values: List[_T]) -> None:
    template = contains(*values)

    assert template == Container(values)


@given(data=st.data(), value=st_anything())
def test_constraint_returns_false(data: st.DataObject, value: _T) -> None:
    values = data.draw(st_values_without(value))

    template = contains(value, *samples(values))

    assert template != Container(values)


@given(values=st_values())
def test_constraint_always_returns_false_when_value_is_not_a_container(values: List[_T]) -> None:
    template = contains(*values)

    assert template != NotContainer()


def test_constraint_raises_value_error_when_less_than_one_value_was_provided() -> None:
    template_partial = partial(contains)

    with pytest.raises(ValueError):
        template_partial()

    with pytest.raises(TooLittleValuesError):
        template_partial()
