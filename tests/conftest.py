import random

from typing import TypeVar, List, Callable
from decimal import Decimal

from hypothesis import strategies as st

_T = TypeVar("_T")
_Ex = TypeVar("_Ex", covariant=True)

Draw = Callable[[st.SearchStrategy[_Ex]], _Ex]

st.register_type_strategy(float, st.floats(allow_nan=False))
st.register_type_strategy(Decimal, st.decimals(allow_nan=False))
st.register_type_strategy(complex, st.complex_numbers(allow_nan=False))


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
