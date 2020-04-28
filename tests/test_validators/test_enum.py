from enum import Enum
from typing import TypeVar, Dict, Callable, Final

import pytest

from hypothesis import given, strategies as st

from testplates.validators import enum_validator, integer_validator
from testplates.validators.exceptions import InvalidTypeError

from tests.conftest import sample, Draw

_T = TypeVar("_T")

EnumFactory = Callable[[Dict[str, _T]], Enum]

uint8: Final = integer_validator(minimum_value=0, maximum_value=255)

# TODO(kprzybyla): Refactor strategies into composites


@pytest.fixture
def enum_factory() -> EnumFactory:
    # noinspection PyArgumentList
    def create(members: Dict[str, _T]) -> Enum:
        return Enum("Example", members)

    return create


@st.composite
def st_uint8(draw: Draw[int]) -> int:
    return draw(st.integers(min_value=0, max_value=255))


@st.composite
def st_negative_integer(draw: Draw[int]) -> int:
    return draw(st.integers(max_value=-1))


@given(members=st.dictionaries(st.text(min_size=1), st_uint8(), min_size=1))
def test_validation_success(enum_factory: EnumFactory, members: Dict[str, _T]) -> None:
    enum_type = enum_factory(members)

    data = sample(enum_type)

    validate = enum_validator(enum_type, uint8)
    error = validate(data)

    assert error is None


@given(members=st.dictionaries(st.text(min_size=1), st_negative_integer(), min_size=1))
def test_validation_failure_due_to_member_validation_error(
    enum_factory: EnumFactory, members: Dict[str, _T]
) -> None:
    enum_type = enum_factory(members)

    with pytest.raises(Exception):
        enum_validator(enum_type, uint8)


@given(members=st.dictionaries(st.text(min_size=1), st_uint8(), min_size=1))
def test_validation_failure_due_to_data_validation_error(
    enum_factory: EnumFactory, members: Dict[str, _T]
) -> None:
    enum_type = enum_factory(members)
    data = sample(enum_type).value

    validate = enum_validator(enum_type)
    error = validate(data)

    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == enum_type


def test_enum_instance_otherness_for_sanity() -> None:
    class Example(Enum):

        VALUE = 0

    class DifferentExample(Enum):

        VALUE = 0

    validate = enum_validator(Example)

    assert validate(Example.VALUE) is None
    assert validate(DifferentExample.VALUE) is not None
