from typing import Any

from hypothesis import given, strategies as st

from testplates.result import Success, Failure
from testplates.boundaries import UNLIMITED
from testplates.validators import integer_validator
from testplates.validators.exceptions import InvalidTypeError, ProhibitedBooleanValueError

from tests.conftest import st_anything_except


@given(data=st.booleans())
def test_success_when_allow_boolean_is_true(data: bool) -> None:
    validator_result = integer_validator(minimum=UNLIMITED, maximum=UNLIMITED, allow_boolean=True)
    validator = Success.get_value(validator_result)

    validation_result = validator(data)
    value = Success.get_value(validation_result)

    assert value is None


@given(data=st_anything_except(int))
def test_failure_when_data_type_validation_fails(data: Any) -> None:
    validator_result = integer_validator(minimum=UNLIMITED, maximum=UNLIMITED)
    validator = Success.get_value(validator_result)

    validation_result = validator(data)
    error = Failure.get_error(validation_result)

    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == (int,)


@given(data=st.booleans())
def test_failure_when_allow_boolean_is_false(data: bool) -> None:
    validator_result = integer_validator(minimum=UNLIMITED, maximum=UNLIMITED)
    validator = Success.get_value(validator_result)

    validation_result = validator(data)
    error = Failure.get_error(validation_result)

    assert isinstance(error, ProhibitedBooleanValueError)
    assert error.data == data
