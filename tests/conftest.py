import random

from typing import TypeVar, List, Iterable, Callable, Final
from decimal import Decimal

from hypothesis import settings, strategies as st

_T = TypeVar("_T")
_Ex = TypeVar("_Ex", covariant=True)

Draw = Callable[[st.SearchStrategy[_Ex]], _Ex]

PROFILE_NO_INCREMENTAL: Final[str] = "no-incremental"

# Use no incremental mode due to multiple issues with hypothesis
# shrinking mechanism which eventually leads to random tests hanging
settings.register_profile(PROFILE_NO_INCREMENTAL, database=None)
settings.load_profile(PROFILE_NO_INCREMENTAL)

# Do not generate NaN value in Decimal since it does not support
# comparison and raises InvalidOperation exception upon comparison
st.register_type_strategy(Decimal, st.decimals(allow_nan=False))


def sample(data: Iterable[_T]) -> _T:
    return random.choice(list(data))


def samples(values: List[_T], minimum: int = 0) -> List[_T]:
    return random.sample(values, k=random.randint(minimum, len(values)))


def st_anything_comparable() -> st.SearchStrategy[_Ex]:
    def filter_anything_comparable(value: _T) -> bool:
        return value == value

    return st.from_type(type).flatmap(st.from_type).filter(filter_anything_comparable)


def st_anything_except(*types: type) -> st.SearchStrategy[_Ex]:
    def filter_anything_except(value: _T) -> bool:
        return value == value and not isinstance(value, types)

    return st.from_type(type).flatmap(st.from_type).filter(filter_anything_except)


def st_anything_except_classinfo() -> st.SearchStrategy[_Ex]:
    def filter_classinfo(value: _T) -> bool:
        try:
            isinstance(object, value)
        except TypeError:
            return value == value
        else:
            return False

    return st.from_type(type).flatmap(st.from_type).filter(filter_classinfo)


def st_anytype_except_type_of(value: _T) -> st.SearchStrategy[_Ex]:
    def filter_anytype_except(type_: type) -> bool:
        return not issubclass(type(value), type_)

    return st.from_type(type).flatmap(st.from_type).map(type).filter(filter_anytype_except)
