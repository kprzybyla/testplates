from enum import Enum, EnumMeta
from typing import cast, TypeVar, Dict, Final

import pytest

from hypothesis import given, strategies as st

from testplates.validators import enum_validator, integer_validator
from testplates.validators.exceptions import InvalidTypeError

from tests.conftest import sample, Draw

_T = TypeVar("_T")

uint8: Final = integer_validator(minimum_value=0, maximum_value=255)


def create_enum(members: Dict[str, _T]) -> EnumMeta:
    return cast(EnumMeta, Enum("Enum", members))


@st.composite
def st_uint8(draw: Draw[int]) -> int:
    return draw(st.integers(min_value=0, max_value=255))


@st.composite
def st_negative_integer(draw: Draw[int]) -> int:
    return draw(st.integers(max_value=-1))


@given(members=st.dictionaries(st.text(min_size=1), st_uint8(), min_size=1))
def test_validation_success(members: Dict[str, _T]) -> None:
    enum = create_enum(members)
    validate = enum_validator(enum, uint8)

    member: Enum = sample(enum)
    error = validate(member)

    assert error is None


@given(members=st.dictionaries(st.text(min_size=1), st_negative_integer(), min_size=1))
def test_validation_failure_due_to_member_validation_error(members: Dict[str, _T]) -> None:
    enum = create_enum(members)

    with pytest.raises(Exception):
        enum_validator(enum, uint8)


@given(members=st.dictionaries(st.text(min_size=1), st_uint8(), min_size=1))
def test_validation_failure_due_to_data_validation_error(members: Dict[str, _T]) -> None:
    enum = create_enum(members)
    validate = enum_validator(enum)

    member: Enum = sample(enum)
    error = validate(member.value)

    assert isinstance(error, InvalidTypeError)
    assert error.data == member.value
    assert error.allowed_types == enum


def test_enum_instance_otherness_for_sanity() -> None:
    class Example(Enum):

        VALUE = 0

    class DifferentExample(Enum):

        VALUE = 0

    validate = enum_validator(Example)

    assert validate(Example.VALUE) is None
    assert validate(DifferentExample.VALUE) is not None
