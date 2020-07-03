from enum import Enum, EnumMeta
from typing import cast, TypeVar, Dict, Final

from hypothesis import given, strategies as st

from testplates.validators import enum_validator, passthrough_validator, integer_validator
from testplates.validators.exceptions import (
    InvalidTypeValueError,
    InvalidTypeError,
    MemberValidationError,
)

from tests.conftest import sample, Draw

_T = TypeVar("_T")

uint8: Final = integer_validator(minimum_value=0, maximum_value=255).value


def create_enum_type(members: Dict[str, _T]) -> EnumMeta:
    return cast(EnumMeta, Enum("Custom", members))


@st.composite
def st_uint8(draw: Draw[int]) -> int:
    return draw(st.integers(min_value=0, max_value=255))


@st.composite
def st_negative_integer(draw: Draw[int]) -> int:
    return draw(st.integers(max_value=-1))


# noinspection PyTypeChecker
@given(members=st.dictionaries(st.text(min_size=1), st_uint8(), min_size=1))
def test_repr(members: Dict[str, _T]) -> None:
    fmt = "testplates.enum_validator({type}, {validator})"

    enum_type = create_enum_type(members)
    validator = enum_validator(enum_type)

    assert repr(validator.value) == fmt.format(type=enum_type, validator=passthrough_validator)


# noinspection PyTypeChecker
@given(members=st.dictionaries(st.text(min_size=1), st_uint8(), min_size=1))
def test_repr_with_member_validator(members: Dict[str, _T]) -> None:
    fmt = "testplates.enum_validator({type}, {validator})"

    enum_type = create_enum_type(members)
    validator = enum_validator(enum_type, uint8)

    assert repr(validator.value) == fmt.format(type=enum_type, validator=uint8)


# noinspection PyTypeChecker
@given(members=st.dictionaries(st.text(min_size=1), st_uint8(), min_size=1))
def test_success(members: Dict[str, _T]) -> None:
    enum_type = create_enum_type(members)
    validator = enum_validator(enum_type, uint8)

    assert not validator.is_failure

    member: Enum = sample(enum_type)
    result = validator.value(member)

    assert not result.is_failure


# noinspection PyTypeChecker
@given(members=st.dictionaries(st.text(min_size=1), st_negative_integer(), min_size=1))
def test_failure_when_member_validation_fails(members: Dict[str, _T]) -> None:
    enum_type = create_enum_type(members)
    validator = enum_validator(enum_type, uint8)

    assert validator.is_failure

    error = validator.error

    assert isinstance(error, MemberValidationError)
    assert error.enum_type == enum_type
    assert error.member in enum_type
    assert isinstance(error.error, Exception)


# noinspection PyTypeChecker
@given(members=st.dictionaries(st.text(min_size=1), st_uint8(), min_size=1))
def test_failure_when_data_validation_fails(members: Dict[str, _T]) -> None:
    enum_type = create_enum_type(members)
    validator = enum_validator(enum_type)

    assert not validator.is_failure

    member: Enum = sample(enum_type)
    result = validator.value(member.value)

    assert result.is_failure

    error = result.error

    assert isinstance(error, InvalidTypeError)
    assert error.data == member.value
    assert error.allowed_types == (enum_type,)


# noinspection PyTypeChecker
def test_failure_when_enum_type_is_not_a_classinfo() -> None:
    class Example:

        __members__ = {}

    enum_type = Example()
    validator = enum_validator(enum_type)  # type: ignore

    assert validator.is_failure

    error = validator.error

    assert isinstance(error, InvalidTypeValueError)
    assert error.given_type == enum_type


def test_enum_instance_otherness_sanity() -> None:
    class Example(Enum):
        VALUE = 0

    class DifferentExample(Enum):
        VALUE = 0

    validator = enum_validator(Example)

    assert not validator.is_failure
    assert validator.value(Example.VALUE).is_failure is False
    assert validator.value(DifferentExample.VALUE).is_failure is True
