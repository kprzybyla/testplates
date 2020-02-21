import random

from typing import TypeVar, List

import pytest

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import is_one_of, NotEnoughValuesError

from .conftest import st_anything, Draw

_T = TypeVar("_T")


@st.composite
def st_values(draw: Draw) -> List[_T]:
    return draw(st.lists(st_anything(), min_size=1))


@st.composite
def st_values_without(draw: Draw, value: _T) -> List[_T]:
    values = draw(st.lists(st_anything(), min_size=1))
    assume(value not in values)

    return values


@given(values=st_values())
def test_is_one_of_returns_true(values: List[_T]) -> None:
    value = random.choice(values)

    assert is_one_of(*values) == value


@given(data=st.data(), value=st_anything())
def test_is_one_of_returns_false(data: st.DataObject, value: _T) -> None:
    values = data.draw(st_values_without(value))

    assert is_one_of(*values) != value


def test_is_one_of_raises_value_error_when_no_values_were_provided() -> None:
    with pytest.raises(ValueError):
        is_one_of()

    with pytest.raises(NotEnoughValuesError):
        is_one_of()
