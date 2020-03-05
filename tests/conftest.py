import random

from typing import TypeVar, List, Callable
from decimal import Decimal
from numbers import Complex

import pytest

from hypothesis import strategies as st

import testplates

from .assets import ObjectStorage, MappingStorage

_T = TypeVar("_T")
_Ex = TypeVar("_Ex", covariant=True)

Draw = Callable[[st.SearchStrategy[_Ex]], _Ex]

st.register_type_strategy(float, st.floats(allow_nan=False))
st.register_type_strategy(Decimal, st.decimals(allow_nan=False))
st.register_type_strategy(Complex, st.complex_numbers(allow_nan=False))


template_parameters = pytest.mark.parametrize(
    "template_type",
    [
        pytest.param(testplates.Object, id="object", marks=pytest.mark.object),
        pytest.param(testplates.Mapping, id="mapping", marks=pytest.mark.mapping),
    ],
)

template_and_storage_parameters = pytest.mark.parametrize(
    "template_type, storage_type",
    [
        pytest.param(testplates.Object, ObjectStorage, id="object", marks=pytest.mark.object),
        pytest.param(testplates.Mapping, MappingStorage, id="mapping", marks=pytest.mark.mapping),
    ],
)


def samples(values: List[_T]) -> List[_T]:
    return random.sample(values, k=random.randint(0, len(values)))


def st_anything() -> st.SearchStrategy[_T]:
    return st.from_type(type).flatmap(st.from_type).filter(lambda x: x == x)


def st_anything_except(*types: type) -> st.SearchStrategy[_T]:
    return st.from_type(type).flatmap(st.from_type).filter(lambda x: not isinstance(x, types))
