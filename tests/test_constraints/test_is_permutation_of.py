import random

from typing import (
    TypeVar,
    Sized,
    Iterable,
    Iterator,
    Container,
    Collection,
    List,
)

from resultful import unwrap_success

from hypothesis import (
    assume,
    given,
    strategies as st,
)

from testplates import is_permutation_of

from tests.utils import samples

from tests.strategies import (
    st_anything_comparable,
    Draw,
)

_T = TypeVar("_T")


class CollectionWrapper(Collection[_T]):

    __slots__ = ("values",)

    def __init__(self, values: List[_T]) -> None:
        self.values = values

    def __len__(self) -> int:
        return len(self.values)

    def __iter__(self) -> Iterator[_T]:
        return iter(self.values)

    def __contains__(self, item: object) -> bool:
        return item in self.values


class NotSized(Iterable[_T], Container[_T]):

    __slots__ = ("values",)

    __len__ = None

    def __init__(self, values: List[_T]) -> None:
        self.values = values

    def __iter__(self) -> Iterator[_T]:
        return iter(self.values)

    def __contains__(self, item: object) -> bool:
        return item in self.values


class NotIterable(Sized, Container[_T]):

    __slots__ = ("values",)

    __iter__ = None

    def __init__(self, values: List[_T]) -> None:
        self.values = values

    def __len__(self) -> int:
        return len(self.values)

    def __contains__(self, item: object) -> bool:
        return item in self.values


class NotContainer(Sized, Iterable[_T]):

    __slots__ = ("values",)

    __contains__ = None

    def __init__(self, values: List[_T]) -> None:
        self.values = values

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
def st_values(draw: Draw[List[_T]], min_size: int = 0) -> List[_T]:
    return draw(st.lists(st_value(), min_size=min_size))


# noinspection PyTypeChecker
@given(values=st_values())
def test_repr(values: List[_T]) -> None:
    fmt = "testplates.is_permutation_of({values})"

    assert (result := is_permutation_of(values))

    constraint = unwrap_success(result)
    assert repr(constraint) == fmt.format(values=repr(values))


# noinspection PyTypeChecker
@given(values=st_values())
def test_returns_true(values: List[_T]) -> None:
    permutation = shuffle(values)

    assert (result := is_permutation_of(permutation))

    constraint = unwrap_success(result)
    assert constraint == CollectionWrapper(values)


# noinspection PyTypeChecker
@given(values=st_values(min_size=1), other=st_value())
def test_returns_false(values: List[_T], other: _T) -> None:
    assume(other not in values)

    index = random_index(values)

    permutation = shuffle(values)
    permutation[index] = other

    assert (result := is_permutation_of(permutation))

    constraint = unwrap_success(result)
    assert constraint != CollectionWrapper(values)


# noinspection PyTypeChecker
@given(values=st_values())
def test_returns_false_when_permutation_has_more_values(values: List[_T]) -> None:
    permutation = values.copy()
    permutation.extend(samples(values))

    assume(len(permutation) > len(values))

    assert (result := is_permutation_of(permutation))

    constraint = unwrap_success(result)
    assert constraint != CollectionWrapper(values)


# noinspection PyTypeChecker
@given(values=st_values())
def test_returns_false_when_permutation_has_fewer_values(values: List[_T]) -> None:
    permutation = samples(values)

    assume(len(permutation) < len(values))

    assert (result := is_permutation_of(permutation))

    constraint = unwrap_success(result)
    assert constraint != CollectionWrapper(values)


# noinspection PyTypeChecker
@given(values=st_values())
def test_returns_false_when_value_is_not_sized(values: List[_T]) -> None:
    assert (result := is_permutation_of(values))

    constraint = unwrap_success(result)
    assert constraint != NotSized(values)


# noinspection PyTypeChecker
@given(values=st_values())
def test_returns_false_when_value_is_not_iterable(values: List[_T]) -> None:
    assert (result := is_permutation_of(values))

    constraint = unwrap_success(result)
    assert constraint != NotIterable(values)


# noinspection PyTypeChecker
@given(values=st_values())
def test_returns_false_when_value_is_not_container(values: List[_T]) -> None:
    assert (result := is_permutation_of(values))

    constraint = unwrap_success(result)
    assert constraint != NotContainer(values)
