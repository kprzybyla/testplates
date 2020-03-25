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
    strategy = st.from_type(type).flatmap(st.from_type)

    return strategy.filter(lambda x: x == x)  # type: ignore


def st_anything_except(*types: type) -> st.SearchStrategy[_Ex]:
    strategy = st.from_type(type).flatmap(st.from_type)

    return strategy.filter(lambda x: not isinstance(x, types))  # type: ignore
