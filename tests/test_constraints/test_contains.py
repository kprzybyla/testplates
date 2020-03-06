from typing import TypeVar, Generic, List
from typing_extensions import Final
from dataclasses import dataclass

import pytest

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import contains, TooLittleValuesError

from ..conftest import samples, st_anything, Draw

_T = TypeVar("_T")

MINIMUM_NUMBER_OF_VALUES: Final[int] = 1


@dataclass
class Container(Generic[_T]):

    values: List[_T]

    def __contains__(self, item: _T) -> bool:
        return item in self.values


class NotContainer:

    __contains__ = None


@st.composite
def st_value(draw: Draw) -> _T:
    return draw(st_anything())


@st.composite
def st_values(draw: Draw) -> List[_T]:
    return draw(st.lists(st_value(), min_size=MINIMUM_NUMBER_OF_VALUES))


@st.composite
def st_values_without(draw: Draw, value: _T) -> List[_T]:
    values = draw(st.lists(st_value()))
    assume(value not in values)

    return values


@given(values=st_values())
def test_returns_true(values: List[_T]) -> None:
    template = contains(*values)

    assert template == Container(values)


@given(data=st.data(), value=st_value())
def test_returns_false(data: st.DataObject, value: _T) -> None:
    values = data.draw(st_values_without(value))

    template = contains(value, *samples(values))

    assert template != Container(values)


@given(values=st_values())
def test_returns_false_when_value_is_not_a_container(values: List[_T]) -> None:
    template = contains(*values)

    assert template != NotContainer()


def test_raises_error_when_less_than_one_value_was_provided() -> None:
    with pytest.raises(TooLittleValuesError):
        contains()
