from typing import TypeVar

from hypothesis import given, strategies as st

from testplates.validators import type_validator
from testplates.validators.exceptions import InvalidTypeValueError, InvalidTypeError

from tests.conftest import (
    st_anything_comparable,
    st_anything_except_classinfo,
    st_anytype_except_type_of,
)

_T = TypeVar("_T")


@given(data=st_anything_comparable())
def test_repr(data: _T) -> None:
    fmt = "testplates.type_validator({type})"

    validator = type_validator(type(data))

    assert repr(validator.value) == fmt.format(type=type(data))


@given(data=st_anything_comparable())
def test_success(data: _T) -> None:
    validator = type_validator(type(data))

    assert not validator.is_failure

    result = validator.value(data)

    assert not result.is_failure


@given(data=st_anything_except_classinfo())
def test_failure_when_type_is_not_a_classinfo(data: _T) -> None:
    validator = type_validator(data)

    assert validator.is_failure, validator

    error = validator.error

    assert isinstance(error, InvalidTypeValueError)
    assert error.given_type == data


@given(st_data=st.data(), data=st_anything_comparable())
def test_failure_when_data_validation_fails(st_data: st.DataObject, data: _T) -> None:
    any_type_except_data = st_data.draw(st_anytype_except_type_of(data))

    validator = type_validator(any_type_except_data)

    assert not validator.is_failure

    result = validator.value(data)

    assert result.is_failure

    error = result.error

    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == (any_type_except_data,)
