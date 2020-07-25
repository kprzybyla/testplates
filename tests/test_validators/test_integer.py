from typing import Any

from hypothesis import given, strategies as st

from testplates import UNLIMITED
from testplates import unwrap_success, unwrap_failure
from testplates import integer_validator
from testplates import InvalidTypeError, ProhibitedBoolValueError

from tests.conftest import st_anything_except


@given(data=st.booleans())
def test_success_when_allow_bool_is_true(data: bool) -> None:
    validator_result = integer_validator(minimum=UNLIMITED, maximum=UNLIMITED, allow_bool=True)
    validator = unwrap_success(validator_result)

    validation_result = validator(data)
    value = unwrap_success(validation_result)

    assert value is None


@given(data=st_anything_except(int))
def test_failure_when_data_type_validation_fails(data: Any) -> None:
    validator_result = integer_validator(minimum=UNLIMITED, maximum=UNLIMITED)
    validator = unwrap_success(validator_result)

    validation_result = validator(data)
    error = unwrap_failure(validation_result)

    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == (int,)


@given(data=st.booleans())
def test_failure_when_allow_bool_is_false(data: bool) -> None:
    validator_result = integer_validator(minimum=UNLIMITED, maximum=UNLIMITED)
    validator = unwrap_success(validator_result)

    validation_result = validator(data)
    error = unwrap_failure(validation_result)

    assert isinstance(error, ProhibitedBoolValueError)
    assert error.data == data
