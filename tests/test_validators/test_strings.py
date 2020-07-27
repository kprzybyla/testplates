from typing import TypeVar

from hypothesis import given, strategies as st

from testplates import UNLIMITED
from testplates import unwrap_success, unwrap_failure
from testplates import string_validator
from testplates import InvalidTypeError

from tests.conftest import st_anything_except

_T = TypeVar("_T")


def test_repr() -> None:
    fmt = "testplates.StringValidator()"

    validator_result = string_validator(minimum_length=UNLIMITED, maximum_length=UNLIMITED)
    validator = unwrap_success(validator_result)

    assert repr(validator) == fmt


@given(data=st.text())
def test_success(data: str) -> None:
    validator_result = string_validator(minimum_length=UNLIMITED, maximum_length=UNLIMITED)
    validator = unwrap_success(validator_result)

    validation_result = validator(data)
    value = unwrap_success(validation_result)

    assert value is None


@given(data=st_anything_except(str))
def test_failure_when_data_validation_fails(data: _T) -> None:
    validator_result = string_validator(minimum_length=UNLIMITED, maximum_length=UNLIMITED)
    validator = unwrap_success(validator_result)

    validation_result = validator(data)
    error = unwrap_failure(validation_result)

    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == (str,)
