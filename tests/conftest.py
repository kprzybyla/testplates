import random

from typing import TypeVar, List, Callable, Final
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


def samples(values: List[_T], minimum: int = 0) -> List[_T]:
    return random.sample(values, k=random.randint(minimum, len(values)))


def st_anything_comparable() -> st.SearchStrategy[_Ex]:
    def filter_anything_comparable(value: _T) -> bool:
        return value == value

    return st.from_type(type).flatmap(st.from_type).filter(filter_anything_comparable)


def st_anything_except(*types: type) -> st.SearchStrategy[_Ex]:
    def filter_anything_except(value: _T) -> bool:
        return not isinstance(value, types)

    return st.from_type(type).flatmap(st.from_type).filter(filter_anything_except)
