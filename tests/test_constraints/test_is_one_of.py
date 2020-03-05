import random

from typing import TypeVar, List

import pytest

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import is_one_of, TooLittleValuesError

from ..conftest import st_anything, Draw

_T = TypeVar("_T")


@st.composite
def st_values(draw: Draw) -> List[_T]:
    return draw(st.lists(st_anything(), min_size=2))


@st.composite
def st_values_without(draw: Draw, value: _T) -> List[_T]:
    values = draw(st.lists(st_anything(), min_size=2))
    assume(value not in values)

    return values


@given(values=st_values())
def test_constraint_returns_true(values: List[_T]) -> None:
    value = random.choice(values)

    template = is_one_of(*values)

    assert template == value


@given(data=st.data(), value=st_anything())
def test_constraint_returns_false(data: st.DataObject, value: _T) -> None:
    values = data.draw(st_values_without(value))

    template = is_one_of(*values)

    assert template != value


@given(values=st.lists(st_anything(), max_size=1))
def test_constraint_raises_value_error_when_less_than_two_values_were_provided(
    values: List[_T]
) -> None:
    with pytest.raises(TooLittleValuesError):
        is_one_of(*values)
