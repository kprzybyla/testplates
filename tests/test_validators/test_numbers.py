from typing import TypeVar, Tuple, Union, Callable, Optional

import pytest

from hypothesis import assume, given, strategies as st

from testplates.validators import any_number_validator, integer_validator, float_validator
from testplates.validators.exceptions import (
    InvalidTypeError,
    ProhibitedBooleanValueError,
    InvalidMinimumValueError,
    InvalidMaximumValueError,
)

from tests.conftest import st_anything_except, st_floats_without_nan

_T = TypeVar("_T")

Validator = Callable[..., Callable[[_T], Optional[Exception]]]
Strategy = Callable[..., st.SearchStrategy[_T]]

validators_and_strategies_parameters = pytest.mark.parametrize(
    "validator, strategy",
    [
        pytest.param(any_number_validator, st.integers, id="any number with integers"),
        pytest.param(any_number_validator, st_floats_without_nan, id="any number with floats"),
        pytest.param(integer_validator, st.integers, id="integer with integers"),
        pytest.param(float_validator, st_floats_without_nan, id="float with floats"),
    ],
)

validators_and_types_parameters = pytest.mark.parametrize(
    "validator, types",
    [
        pytest.param(any_number_validator, (int, float), id="any_number_validator"),
        pytest.param(integer_validator, int, id="integer_validator"),
        pytest.param(float_validator, float, id="float_validator"),
    ],
)

integer_validators_parameters = pytest.mark.parametrize(
    "validator",
    [
        pytest.param(any_number_validator, id="any_number_validator"),
        pytest.param(integer_validator, id="integer_validator"),
    ],
)


# TODO(kprzybyla): Think about test where any_number_validator is used and maximum
#                  value is float and data type is int. Should we allow such things?

# TODO(kprzybyla): Add tests with exclusive boundaries mixed with other boundaries etc?

# TODO(kprzybyla): Verify that everything is tested


@given(st_data=st.data())
@validators_and_strategies_parameters
def test_validation_success(
    validator: Validator, strategy: Strategy, st_data: st.DataObject
) -> None:
    data = st_data.draw(strategy())

    validate = validator()
    error = validate(data)

    assert error is None


@given(st_data=st.data())
@validators_and_strategies_parameters
def test_validation_success_with_minimum(
    validator: Validator, strategy: Strategy, st_data: st.DataObject
) -> None:
    data = st_data.draw(strategy())
    minimum_value = st_data.draw(strategy(max_value=data))

    validate = validator(minimum_value=minimum_value)
    error = validate(data)

    assert error is None


@given(st_data=st.data())
@validators_and_strategies_parameters
def test_validation_success_with_maximum(
    validator: Validator, strategy: Strategy, st_data: st.DataObject
) -> None:
    data = st_data.draw(strategy())
    maximum_value = st_data.draw(strategy(min_value=data))

    validate = validator(maximum_value=maximum_value)
    error = validate(data)

    assert error is None


@given(st_data=st.data())
@validators_and_strategies_parameters
def test_validation_success_with_minimum_and_maximum(
    validator: Validator, strategy: Strategy, st_data: st.DataObject
) -> None:
    data = st_data.draw(strategy())

    minimum_value = st_data.draw(strategy(max_value=data))
    maximum_value = st_data.draw(strategy(min_value=data))

    assume(minimum_value != maximum_value)

    validate = validator(minimum_value=minimum_value, maximum_value=maximum_value)
    error = validate(data)

    assert error is None


@given(st_data=st.data())
@validators_and_strategies_parameters
def test_validation_failure_with_minimum(
    validator: Validator, strategy: Strategy, st_data: st.DataObject
) -> None:
    data = st_data.draw(strategy())
    minimum_value = st_data.draw(strategy(min_value=data))

    assume(minimum_value != data)

    validate = validator(minimum_value=minimum_value)
    error = validate(data)

    assert isinstance(error, InvalidMinimumValueError)
    assert error.data == data
    assert error.minimum.value == minimum_value


@given(st_data=st.data())
@validators_and_strategies_parameters
def test_validation_failure_with_maximum(
    validator: Validator, strategy: Strategy, st_data: st.DataObject
) -> None:
    data = st_data.draw(strategy())
    maximum_value = st_data.draw(strategy(max_value=data))

    assume(maximum_value != data)

    validate = validator(maximum_value=maximum_value)
    error = validate(data)

    assert isinstance(error, InvalidMaximumValueError)
    assert error.data == data
    assert error.maximum.value == maximum_value


@given(st_data=st.data())
@validators_and_strategies_parameters
def test_validation_failure_with_exclusive_minimum(
    validator: Validator, strategy: Strategy, st_data: st.DataObject
) -> None:
    data = st_data.draw(strategy())
    minimum_value = st_data.draw(strategy(min_value=data))

    validate = validator(exclusive_minimum_value=minimum_value)
    error = validate(data)

    assert isinstance(error, InvalidMinimumValueError)
    assert error.data == data
    assert error.minimum.value == minimum_value


@given(st_data=st.data())
@validators_and_strategies_parameters
def test_validation_failure_with_exclusive_maximum(
    validator: Validator, strategy: Strategy, st_data: st.DataObject
) -> None:
    data = st_data.draw(strategy())
    maximum_value = st_data.draw(strategy(max_value=data))

    validate = validator(exclusive_maximum_value=maximum_value)
    error = validate(data)

    assert isinstance(error, InvalidMaximumValueError)
    assert error.data == data
    assert error.maximum.value == maximum_value


@given(st_data=st.data())
@validators_and_types_parameters
def test_validation_failure_due_to_invalid_type(
    validator: Validator, types: Union[type, Tuple[type, ...]], st_data: st.DataObject
) -> None:
    data = st_data.draw(st_anything_except(types))

    validate = validator()
    error = validate(data)

    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == types


@given(data=st.booleans())
@integer_validators_parameters
def test_integer_validation_success_with_boolean_data(validator: Validator, data: bool) -> None:
    validate = validator(allow_boolean=True)
    error = validate(data)

    assert error is None


@given(data=st.booleans())
@integer_validators_parameters
def test_integer_validation_failure_due_to_boolean_data(validator: Validator, data: bool) -> None:
    validate = validator()
    error = validate(data)

    assert isinstance(error, ProhibitedBooleanValueError)
    assert error.data == data
