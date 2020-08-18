from typing import TypeVar

from resultful import unwrap_success, unwrap_failure
from hypothesis import given
from hypothesis import strategies as st

from testplates import boolean_validator
from testplates import InvalidTypeError

from tests.strategies import st_anything_except

_T = TypeVar("_T")


def test_repr() -> None:
    assert (validator_result := boolean_validator())

    fmt = "testplates.boolean_validator()"
    validator = unwrap_success(validator_result)
    assert repr(validator) == fmt


@given(data=st.booleans())
def test_success(data: bool) -> None:
    assert (validator_result := boolean_validator())

    validator = unwrap_success(validator_result)
    assert (validation_result := validator(data))

    outcome = unwrap_success(validation_result)
    assert outcome is None


@given(data=st_anything_except(bool))
def test_failure_when_data_validation_fails(data: _T) -> None:
    assert (validator_result := boolean_validator())

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == (bool,)
