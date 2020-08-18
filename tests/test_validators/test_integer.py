from typing import Any

from resultful import unwrap_success, unwrap_failure
from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import UNLIMITED
from testplates import integer_validator
from testplates import (
    InvalidTypeError,
    ProhibitedBoolValueError,
    InvalidMinimumValueError,
    InvalidMaximumValueError,
)

from tests.strategies import st_anything_except


def test_repr() -> None:
    raise NotImplementedError()


@given(data=st.booleans())
def test_success_when_allow_bool_is_true(data: bool) -> None:
    assert (
        validator_result := integer_validator(
            minimum=UNLIMITED, maximum=UNLIMITED, allow_bool=True,
        )
    )

    validator = unwrap_success(validator_result)
    assert (validation_result := validator(data))

    outcome = unwrap_success(validation_result)
    assert outcome is None


@given(data=st_anything_except(int))
def test_failure_when_data_type_validation_fails(data: Any) -> None:
    assert (validator_result := integer_validator(minimum=UNLIMITED, maximum=UNLIMITED))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == (int,)


@given(data=st.booleans())
def test_failure_when_allow_bool_is_false(data: bool) -> None:
    assert (validator_result := integer_validator(minimum=UNLIMITED, maximum=UNLIMITED))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, ProhibitedBoolValueError)
    assert error.data == data


@given(st_data=st.data(), data=st.integers())
def test_failure_when_value_does_not_fit_minimum_value(st_data: st.DataObject, data: int) -> None:
    minimum = st_data.draw(st.integers(min_value=data))

    assume(data < minimum)

    assert (validator_result := integer_validator(minimum=minimum, maximum=UNLIMITED))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidMinimumValueError)
    assert error.data == data
    assert error.minimum.value == minimum


@given(st_data=st.data(), data=st.integers())
def test_failure_when_value_does_not_fit_maximum_value(st_data: st.DataObject, data: int) -> None:
    maximum = st_data.draw(st.integers(max_value=data))

    assume(data > maximum)

    assert (validator_result := integer_validator(minimum=UNLIMITED, maximum=maximum))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidMaximumValueError)
    assert error.data == data
    assert error.maximum.value == maximum
