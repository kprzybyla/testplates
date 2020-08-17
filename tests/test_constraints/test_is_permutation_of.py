import random

from typing import TypeVar, Sized, Iterable, Iterator, Container, Collection, List, Final
from dataclasses import dataclass

import pytest

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import is_permutation_of
from testplates import InsufficientValuesError

from tests.utils import samples
from tests.strategies import st_anything_comparable, Draw

_T = TypeVar("_T")

MINIMUM_NUMBER_OF_VALUES: Final[int] = 2


@dataclass
class CollectionWrapper(Collection[_T]):

    values: List[_T]

    def __len__(self) -> int:
        return len(self.values)

    def __iter__(self) -> Iterator[_T]:
        return iter(self.values)

    def __contains__(self, item: object) -> bool:
        return item in self.values


@dataclass
class NotSized(Iterable[_T], Container[_T]):

    values: List[_T]

    __len__ = None

    def __iter__(self) -> Iterator[_T]:
        return iter(self.values)

    def __contains__(self, item: object) -> bool:
        return item in self.values


@dataclass
class NotIterable(Sized, Container[_T]):

    values: List[_T]

    __iter__ = None

    def __len__(self) -> int:
        return len(self.values)

    def __contains__(self, item: object) -> bool:
        return item in self.values


@dataclass
class NotContainer(Sized, Iterable[_T]):

    values: List[_T]

    __contains__ = None

    def __len__(self) -> int:
        return len(self.values)

    def __iter__(self) -> Iterator[_T]:
        return iter(self.values)


def shuffle(values: List[_T]) -> List[_T]:
    shuffled = values.copy()
    random.shuffle(shuffled)

    return shuffled


def random_index(values: List[_T]) -> int:
    return random.randrange(0, len(values))


@st.composite
def st_value(draw: Draw[_T]) -> _T:
    return draw(st_anything_comparable())


@st.composite
def st_values(draw: Draw[List[_T]]) -> List[_T]:
    return draw(st.lists(st_value(), min_size=MINIMUM_NUMBER_OF_VALUES))


@st.composite
def st_inverse_values(draw: Draw[List[_T]]) -> List[_T]:
    values = draw(st.lists(st_value(), max_size=MINIMUM_NUMBER_OF_VALUES))
    assume(len(values) != MINIMUM_NUMBER_OF_VALUES)

    return values


# noinspection PyTypeChecker
@given(values=st_values())
def test_repr(values: List[_T]) -> None:
    fmt = "testplates.IsPermutationOf({values})"

    constraint = is_permutation_of(values)

    assert repr(constraint) == fmt.format(values=repr(values))


# noinspection PyTypeChecker
@given(values=st_values())
def test_returns_true(values: List[_T]) -> None:
    permutation = shuffle(values)

    constraint = is_permutation_of(permutation)

    assert constraint == CollectionWrapper(values)


# noinspection PyTypeChecker
@given(values=st_values(), other=st_value())
def test_returns_false(values: List[_T], other: _T) -> None:
    assume(other not in values)

    index = random_index(values)

    permutation = shuffle(values)
    permutation[index] = other

    constraint = is_permutation_of(permutation)

    assert constraint != CollectionWrapper(values)


# noinspection PyTypeChecker
@given(values=st_values())
def test_returns_false_when_permutation_has_more_values(values: List[_T]) -> None:
    permutation = values.copy()
    permutation.extend(samples(values))

    assume(len(permutation) > len(values))

    constraint = is_permutation_of(permutation)

    assert constraint != CollectionWrapper(values)


# noinspection PyTypeChecker
@given(values=st_values())
def test_returns_false_when_permutation_has_fewer_values(values: List[_T]) -> None:
    permutation = samples(values, minimum=MINIMUM_NUMBER_OF_VALUES)

    assume(len(permutation) < len(values))

    constraint = is_permutation_of(permutation)

    assert constraint != CollectionWrapper(values)


# noinspection PyTypeChecker
@given(values=st_values())
def test_returns_false_when_value_is_not_sized(values: List[_T]) -> None:
    constraint = is_permutation_of(values)

    assert constraint != NotSized(values)


# noinspection PyTypeChecker
@given(values=st_values())
def test_returns_false_when_value_is_not_iterable(values: List[_T]) -> None:
    constraint = is_permutation_of(values)

    assert constraint != NotIterable(values)


# noinspection PyTypeChecker
@given(values=st_values())
def test_returns_false_when_value_is_not_container(values: List[_T]) -> None:
    constraint = is_permutation_of(values)

    assert constraint != NotContainer(values)


# noinspection PyTypeChecker
@given(values=st_inverse_values())
def test_raises_error_when_less_than_two_values_were_provided(values: List[_T]) -> None:
    with pytest.raises(InsufficientValuesError) as exception:
        is_permutation_of(values)

    assert exception.value.required == MINIMUM_NUMBER_OF_VALUES
