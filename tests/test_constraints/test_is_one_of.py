import random

from typing import TypeVar, List, Final

import pytest

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import is_one_of, InsufficientValuesError

from tests.conftest import st_anything_comparable, Draw

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


@st.composite
def st_inverse_values(draw: Draw[List[_T]]) -> List[_T]:
    values = draw(st.lists(st_value(), max_size=MINIMUM_NUMBER_OF_VALUES))
    assume(len(values) != MINIMUM_NUMBER_OF_VALUES)

    return values


@given(values=st_values())
def test_repr(values: List[_T]) -> None:
    fmt = "testplates.IsOneOf({values})"

    constraint = is_one_of(*values)

    assert repr(constraint) == fmt.format(values=", ".join(repr(value) for value in values))


@given(values=st_values())
def test_returns_true(values: List[_T]) -> None:
    value = random.choice(values)

    constraint = is_one_of(*values)

    assert constraint == value


@given(data=st.data(), value=st_value())
def test_returns_false(data: st.DataObject, value: _T) -> None:
    values = data.draw(st_values_without(value))

    constraint = is_one_of(*values)

    assert constraint != value


@given(values=st_inverse_values())
def test_raises_error_when_less_than_two_values_were_provided(values: List[_T]) -> None:
    with pytest.raises(InsufficientValuesError) as exception:
        is_one_of(*values)

    assert exception.value.required == MINIMUM_NUMBER_OF_VALUES
