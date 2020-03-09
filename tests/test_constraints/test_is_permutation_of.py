import random
import itertools

from typing import TypeVar, List
from typing_extensions import Final

import pytest

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import is_permutation_of, TooLittleValuesError

from ..conftest import samples, st_anything, Draw

_T = TypeVar("_T")

MINIMUM_NUMBER_OF_VALUES: Final[int] = 2


class NotIterable:

    __iter__ = None


def shuffle(values: List[_T]) -> List[_T]:
    shuffled = values.copy()
    random.shuffle(shuffled)

    return shuffled


def random_index(values: List[_T]) -> int:
    return random.randrange(0, len(values))


@st.composite
def st_value(draw: Draw) -> _T:
    return draw(st_anything())


@st.composite
def st_values(draw: Draw) -> List[_T]:
    return draw(st.lists(st_value(), min_size=MINIMUM_NUMBER_OF_VALUES))


@st.composite
def st_inverse_values(draw: Draw) -> List[_T]:
    values = draw(st.lists(st_value(), max_size=MINIMUM_NUMBER_OF_VALUES))
    assume(len(values) != MINIMUM_NUMBER_OF_VALUES)

    return values


@given(values=st_values())
def test_returns_true(values: List[_T]) -> None:
    permutation = shuffle(values)

    template = is_permutation_of(permutation)

    assert template == values


@given(values=st_values(), other=st_value())
def test_returns_false(values: List[_T], other: _T) -> None:
    assume(other not in values)

    index = random_index(values)

    permutation = shuffle(values)
    permutation[index] = other

    template = is_permutation_of(permutation)

    assert template != values


@given(values=st_values())
def test_returns_false_when_permutation_has_more_values(values: List[_T]) -> None:
    permutation = values.copy()
    permutation.extend(samples(values))

    assume(len(permutation) > len(values))

    template = is_permutation_of(permutation)

    assert template != values


@given(values=st_values())
def test_returns_false_when_permutation_has_fewer_values(values: List[_T]) -> None:
    permutation = samples(values, minimum=MINIMUM_NUMBER_OF_VALUES)

    assume(len(permutation) < len(values))

    template = is_permutation_of(permutation)

    assert template != values


@given(values=st_values())
def test_returns_false_when_value_is_not_iterable(values: List[_T]) -> None:
    template = is_permutation_of(values)

    assert template != NotIterable()


@given(values=st_inverse_values())
def test_raises_error_when_less_than_two_values_were_provided(values: List[_T]) -> None:
    with pytest.raises(TooLittleValuesError):
        is_permutation_of(values)
