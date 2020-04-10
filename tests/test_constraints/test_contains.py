from typing import TypeVar, List, Container, Final
from dataclasses import dataclass

import pytest

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import contains, InsufficientValuesError

from tests.conftest import samples, st_anything_comparable, Draw

_T = TypeVar("_T")

MINIMUM_NUMBER_OF_VALUES: Final[int] = 1


@dataclass
class ContainerWrapper(Container[_T]):

    values: List[_T]

    def __contains__(self, item: object) -> bool:
        return item in self.values


class NotContainer:

    __contains__ = None


@st.composite
def st_value(draw: Draw[_T]) -> _T:
    return draw(st_anything_comparable())


@st.composite
def st_values(draw: Draw[List[_T]]) -> List[_T]:
    return draw(st.lists(st_value(), min_size=MINIMUM_NUMBER_OF_VALUES))


@st.composite
def st_values_without(draw: Draw[List[_T]], value: _T) -> List[_T]:
    values = draw(st.lists(st_value()))
    assume(value not in values)

    return values


@given(values=st_values())
def test_repr(values: List[_T]) -> None:
    fmt = "testplates.contains({values})"

    constraint = contains(*values)

    assert repr(constraint) == fmt.format(values=", ".join(repr(value) for value in values))


@given(values=st_values())
def test_returns_true(values: List[_T]) -> None:
    constraint = contains(*values)

    assert constraint == ContainerWrapper(values)


@given(data=st.data(), value=st_value())
def test_returns_false(data: st.DataObject, value: _T) -> None:
    values = data.draw(st_values_without(value))

    constraint = contains(value, *samples(values))

    assert constraint != ContainerWrapper(values)


@given(values=st_values())
def test_returns_false_when_value_is_not_container(values: List[_T]) -> None:
    constraint = contains(*values)

    assert constraint != NotContainer()


def test_raises_error_when_less_than_one_value_was_provided() -> None:
    with pytest.raises(InsufficientValuesError):
        contains()
