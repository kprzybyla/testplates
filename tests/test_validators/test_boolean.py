from typing import TypeVar

from hypothesis import given, strategies as st

from testplates import Success, Failure
from testplates.validators import boolean_validator
from testplates.validators.exceptions import InvalidTypeError

from tests.conftest import st_anything_except

_T = TypeVar("_T")


def test_repr() -> None:
    fmt = "testplates.boolean_validator()"

    validator_result = boolean_validator()
    validator = Success.get_value(validator_result)

    assert repr(validator) == fmt


@given(data=st.booleans())
def test_success(data: bool) -> None:
    validator_result = boolean_validator()
    validator = Success.get_value(validator_result)

    validation_result = validator(data)
    value = Success.get_value(validation_result)

    assert value is None


@given(data=st_anything_except(bool))
def test_failure_when_data_validation_fails(data: _T) -> None:
    validator_result = boolean_validator()
    validator = Success.get_value(validator_result)

    validation_result = validator(data)
    error = Failure.get_error(validation_result)

    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == (bool,)
