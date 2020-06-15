from enum import Enum, EnumMeta
from typing import cast, TypeVar, Dict, Final

from hypothesis import given, strategies as st

from testplates.validators import enum_validator, integer_validator
from testplates.validators.exceptions import InvalidTypeError, MemberValidationError

from tests.conftest import sample, Draw

_T = TypeVar("_T")

uint8: Final = integer_validator(minimum_value=0, maximum_value=255)


def create_enum_type(members: Dict[str, _T]) -> EnumMeta:
    return cast(EnumMeta, Enum("Custom", members))


@st.composite
def st_uint8(draw: Draw[int]) -> int:
    return draw(st.integers(min_value=0, max_value=255))


@st.composite
def st_negative_integer(draw: Draw[int]) -> int:
    return draw(st.integers(max_value=-1))


@given(members=st.dictionaries(st.text(min_size=1), st_uint8(), min_size=1))
def test_validation_success(members: Dict[str, _T]) -> None:
    enum_type = create_enum_type(members)
    validate = enum_validator(enum_type, uint8)

    member: Enum = sample(enum_type)
    error = validate(member)

    assert error is None


@given(members=st.dictionaries(st.text(min_size=1), st_negative_integer(), min_size=1))
def test_validation_failure_due_to_member_validation_error(members: Dict[str, _T]) -> None:
    enum_type = create_enum_type(members)
    validator = enum_validator(enum_type, uint8)

    assert isinstance(validator, MemberValidationError)
    assert validator.enum_type == enum_type
    assert validator.member in enum_type
    assert isinstance(validator.error, Exception)


@given(members=st.dictionaries(st.text(min_size=1), st_uint8(), min_size=1))
def test_validation_failure_due_to_data_validation_error(members: Dict[str, _T]) -> None:
    enum_type = create_enum_type(members)
    validate = enum_validator(enum_type)

    member: Enum = sample(enum_type)
    error = validate(member.value)

    assert isinstance(error, InvalidTypeError)
    assert error.data == member.value
    assert error.allowed_types == enum_type


def test_enum_instance_otherness_for_sanity() -> None:
    class Example(Enum):

        VALUE = 0

    class DifferentExample(Enum):

        VALUE = 0

    validate = enum_validator(Example)

    assert validate(Example.VALUE) is None
    assert validate(DifferentExample.VALUE) is not None
