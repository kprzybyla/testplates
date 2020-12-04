from typing import (
    Any,
)

from resultful import (
    unwrap_success,
    unwrap_failure,
)

from hypothesis import (
    given,
    strategies as st,
)

from testplates import (
    boolean_validator,
    InvalidTypeError,
)

from tests.strategies import st_anything_except


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
def test_failure_when_data_validation_fails(data: Any) -> None:
    assert (validator_result := boolean_validator())

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == (bool,)
