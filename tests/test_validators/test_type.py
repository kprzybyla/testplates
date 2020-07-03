from typing import TypeVar

from hypothesis import given, strategies as st

from testplates import Success, Failure
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

    validator_result = type_validator(type(data))
    validator = Success.from_result(validator_result).value

    assert repr(validator) == fmt.format(type=type(data))


@given(data=st_anything_comparable())
def test_success(data: _T) -> None:
    validator_result = type_validator(type(data))
    validator = Success.from_result(validator_result).value

    validation_result = validator(data)
    value = Success.from_result(validation_result).value

    assert value is None


@given(data=st_anything_except_classinfo())
def test_failure_when_type_is_not_a_classinfo(data: _T) -> None:
    validator_result = type_validator(data)
    error = Failure.from_result(validator_result).error

    assert isinstance(error, InvalidTypeValueError)
    assert error.given_type == data


@given(st_data=st.data(), data=st_anything_comparable())
def test_failure_when_data_validation_fails(st_data: st.DataObject, data: _T) -> None:
    any_type_except_data = st_data.draw(st_anytype_except_type_of(data))

    validator_result = type_validator(any_type_except_data)
    validator = Success.from_result(validator_result).value

    validation_result = validator(data)
    error = Failure.from_result(validation_result).error

    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == (any_type_except_data,)
