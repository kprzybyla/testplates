import random

from typing import TypeVar, List, Final

from resultful import unwrap_success
from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import is_one_of

from tests.strategies import st_anything_comparable, Draw

_T = TypeVar("_T")

MINIMUM_NUMBER_OF_VALUES: Final[int] = 2


@st.composite
def st_value(draw: Draw[_T]) -> _T:
    return draw(st_anything_comparable())


@st.composite
def st_values(draw: Draw[List[_T]]) -> List[_T]:
    return draw(st.lists(st_value(), min_size=MINIMUM_NUMBER_OF_VALUES))


@st.composite
def st_values_without(draw: Draw[List[_T]], value: _T) -> List[_T]:
    values = draw(st_values())
    assume(value not in values)

    return values


# noinspection PyTypeChecker
# noinspection PyArgumentList
@given(values=st_values())
def test_repr(values: List[_T]) -> None:
    fmt = "testplates.is_one_of({values})"

    assert (result := is_one_of(*values))

    constraint = unwrap_success(result)
    assert repr(constraint) == fmt.format(values=", ".join(repr(value) for value in values))


# noinspection PyTypeChecker
# noinspection PyArgumentList
@given(values=st_values())
def test_returns_true(values: List[_T]) -> None:
    value = random.choice(values)

    assert (result := is_one_of(*values))

    constraint = unwrap_success(result)
    assert constraint == value


# noinspection PyTypeChecker
# noinspection PyArgumentList
@given(data=st.data(), value=st_value())
def test_returns_false(data: st.DataObject, value: _T) -> None:
    values = data.draw(st_values_without(value))

    assert (result := is_one_of(*values))

    constraint = unwrap_success(result)
    assert constraint != value
