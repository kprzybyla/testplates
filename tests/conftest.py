import pytest
import testplates

from typing import Any
from decimal import Decimal
from numbers import Complex

from hypothesis.strategies import (
    floats,
    decimals,
    complex_numbers,
    from_type,
    register_type_strategy,
    SearchStrategy,
)

from .assets import ObjectStorage, MappingStorage

register_type_strategy(float, floats(allow_nan=False))
register_type_strategy(Decimal, decimals(allow_nan=False))
register_type_strategy(Complex, complex_numbers(allow_nan=False))


template_parameters = pytest.mark.parametrize(
    "template_type",
    [
        pytest.param(testplates.types.Object, id="object"),
        pytest.param(testplates.types.Mapping, id="mapping"),
    ],
)

template_and_storage_parameters = pytest.mark.parametrize(
    "template_type, storage_type",
    [
        pytest.param(testplates.types.Object, ObjectStorage, id="object"),
        pytest.param(testplates.types.Mapping, MappingStorage, id="mapping"),
    ],
)


def anything() -> SearchStrategy[Any]:
    return from_type(type).flatmap(from_type).filter(lambda x: x == x)
