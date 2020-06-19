from typing import TypeVar, Tuple, Union, Callable

import pytest

from hypothesis import assume, given, strategies as st

from testplates.result import Result
from testplates.boundaries import UNLIMITED
from testplates.validators import any_number_validator, integer_validator, float_validator
from testplates.validators.exceptions import (
    InvalidTypeError,
    ProhibitedBooleanValueError,
    InvalidMinimumValueError,
    InvalidMaximumValueError,
)

from tests.conftest import st_anything_except, st_floats_without_nan

_T = TypeVar("_T")

Strategy = Callable[..., st.SearchStrategy[_T]]
Validator = Callable[..., Result[Callable[[_T], Result[None]]]]

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


@given(st_data=st.data())
@validators_and_strategies_parameters
def test_validation_success(
    validator: Validator[_T], strategy: Strategy[_T], st_data: st.DataObject
) -> None:
    data = st_data.draw(strategy())

    validate = validator(minimum_value=UNLIMITED, maximum_value=UNLIMITED)
    assert not validate.is_error

    result = validate.value(data)
    assert not result.is_error


@given(st_data=st.data())
@validators_and_strategies_parameters
def test_validation_success_with_minimum(
    validator: Validator[_T], strategy: Strategy[_T], st_data: st.DataObject
) -> None:
    data = st_data.draw(strategy())
    minimum_value = st_data.draw(strategy(max_value=data))

    validate = validator(minimum_value=minimum_value, maximum_value=UNLIMITED)
    assert not validate.is_error

    result = validate.value(data)
    assert not result.is_error


@given(st_data=st.data())
@validators_and_strategies_parameters
def test_validation_success_with_maximum(
    validator: Validator[_T], strategy: Strategy[_T], st_data: st.DataObject
) -> None:
    data = st_data.draw(strategy())
    maximum_value = st_data.draw(strategy(min_value=data))

    validate = validator(minimum_value=UNLIMITED, maximum_value=maximum_value)
    assert not validate.is_error

    result = validate.value(data)
    assert not result.is_error


@given(st_data=st.data())
@validators_and_strategies_parameters
def test_validation_success_with_exclusive_minimum(
    validator: Validator[_T], strategy: Strategy[_T], st_data: st.DataObject
) -> None:
    data = st_data.draw(strategy())
    minimum_value = st_data.draw(strategy(max_value=data))

    assume(minimum_value != data)

    validate = validator(exclusive_minimum_value=minimum_value, maximum_value=UNLIMITED)
    assert not validate.is_error

    result = validate.value(data)
    assert not result.is_error


@given(st_data=st.data())
@validators_and_strategies_parameters
def test_validation_success_with_exclusive_maximum(
    validator: Validator[_T], strategy: Strategy[_T], st_data: st.DataObject
) -> None:
    data = st_data.draw(strategy())
    maximum_value = st_data.draw(strategy(min_value=data))

    assume(maximum_value != data)

    validate = validator(minimum_value=UNLIMITED, exclusive_maximum_value=maximum_value)
    assert not validate.is_error

    result = validate.value(data)
    assert not result.is_error


@given(st_data=st.data())
@validators_and_strategies_parameters
def test_validation_success_with_minimum_and_maximum(
    validator: Validator[_T], strategy: Strategy[_T], st_data: st.DataObject
) -> None:
    data = st_data.draw(strategy())

    minimum_value = st_data.draw(strategy(max_value=data))
    maximum_value = st_data.draw(strategy(min_value=data))

    assume(minimum_value != maximum_value)

    validate = validator(minimum_value=minimum_value, maximum_value=maximum_value)
    assert not validate.is_error

    result = validate.value(data)
    assert not result.is_error


def test_validation_success_with_minimum_and_exclusive_maximum() -> None:
    pass


def test_validation_success_with_exclusive_minimum_and_maximum() -> None:
    pass


def test_validation_success_with_exclusive_minimum_and_exclusive_maximum() -> None:
    pass


@given(st_data=st.data())
@validators_and_strategies_parameters
def test_validation_failure_with_minimum(
    validator: Validator[_T], strategy: Strategy[_T], st_data: st.DataObject
) -> None:
    data = st_data.draw(strategy())
    minimum_value = st_data.draw(strategy(min_value=data))

    assume(minimum_value != data)

    validate = validator(minimum_value=minimum_value, maximum_value=UNLIMITED)
    assert not validate.is_error

    result = validate.value(data)
    assert result.is_error

    error = result.error
    assert isinstance(error, InvalidMinimumValueError)
    assert error.data == data
    assert error.minimum.value == minimum_value


@given(st_data=st.data())
@validators_and_strategies_parameters
def test_validation_failure_with_maximum(
    validator: Validator[_T], strategy: Strategy[_T], st_data: st.DataObject
) -> None:
    data = st_data.draw(strategy())
    maximum_value = st_data.draw(strategy(max_value=data))

    assume(maximum_value != data)

    validate = validator(minimum_value=UNLIMITED, maximum_value=maximum_value)
    assert not validate.is_error

    result = validate.value(data)
    assert result.is_error

    error = result.error
    assert isinstance(error, InvalidMaximumValueError)
    assert error.data == data
    assert error.maximum.value == maximum_value


@given(st_data=st.data())
@validators_and_strategies_parameters
def test_validation_failure_with_exclusive_minimum(
    validator: Validator[_T], strategy: Strategy[_T], st_data: st.DataObject
) -> None:
    data = st_data.draw(strategy())
    minimum_value = st_data.draw(strategy(min_value=data))

    validate = validator(exclusive_minimum_value=minimum_value, maximum_value=UNLIMITED)
    assert not validate.is_error

    result = validate.value(data)
    assert result.is_error

    error = result.error
    assert isinstance(error, InvalidMinimumValueError)
    assert error.data == data
    assert error.minimum.value == minimum_value


@given(st_data=st.data())
@validators_and_strategies_parameters
def test_validation_failure_with_exclusive_maximum(
    validator: Validator[_T], strategy: Strategy[_T], st_data: st.DataObject
) -> None:
    data = st_data.draw(strategy())
    maximum_value = st_data.draw(strategy(max_value=data))

    validate = validator(minimum_value=UNLIMITED, exclusive_maximum_value=maximum_value)
    assert not validate.is_error

    result = validate.value(data)
    assert result.is_error

    error = result.error
    assert isinstance(error, InvalidMaximumValueError)
    assert error.data == data
    assert error.maximum.value == maximum_value


def test_validation_failure_with_upper_minimum_and_maximum() -> None:
    pass


def test_validation_failure_with_lower_minimum_and_maximum() -> None:
    pass


def test_validation_failure_with_upper_minimum_and_exclusive_maximum() -> None:
    pass


def test_validation_failure_with_lower_minimum_and_exclusive_maximum() -> None:
    pass


def test_validation_failure_with_upper_exclusive_minimum_and_maximum() -> None:
    pass


def test_validation_failure_with_lower_exclusive_minimum_and_maximum() -> None:
    pass


def test_validation_failure_with_upper_exclusive_minimum_and_exclusive_maximum() -> None:
    pass


def test_validation_failure_with_lower_exclusive_minimum_and_exclusive_maximum() -> None:
    pass


@given(st_data=st.data())
@validators_and_types_parameters
def test_validation_failure_due_to_invalid_type(
    validator: Validator[_T], types: Union[type, Tuple[type, ...]], st_data: st.DataObject
) -> None:
    data = st_data.draw(st_anything_except(types))

    validate = validator(minimum_value=UNLIMITED, maximum_value=UNLIMITED)
    assert not validate.is_error

    result = validate.value(data)
    assert result.is_error

    error = result.error
    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == types


@given(data=st.booleans())
@integer_validators_parameters
def test_integer_validation_success_with_boolean_data(
    validator: Validator[bool], data: bool
) -> None:
    validate = validator(minimum_value=UNLIMITED, maximum_value=UNLIMITED, allow_boolean=True)
    assert not validate.is_error

    result = validate.value(data)
    assert not result.is_error


@given(data=st.booleans())
@integer_validators_parameters
def test_integer_validation_failure_due_to_boolean_data(
    validator: Validator[bool], data: bool
) -> None:
    validate = validator(minimum_value=UNLIMITED, maximum_value=UNLIMITED)
    assert not validate.is_error

    result = validate.value(data)
    assert result.is_error

    error = result.error
    assert isinstance(error, ProhibitedBooleanValueError)
    assert error.data == data


def test_validation_failure_when_value_does_not_implement_boundaries_with_inclusive_boundaries() -> None:
    pass


def test_validation_failure_when_value_does_not_implement_boundaries_with_exclusive_boundaries() -> None:
    pass


def test_validation_failure_on_missing_boundaries() -> None:
    pass


def test_validation_failure_on_missing_minimum_boundary() -> None:
    pass


def test_validation_failure_on_missing_maximum_boundary() -> None:
    pass


def test_validation_failure_on_mutually_exclusive_boundaries() -> None:
    pass


def test_validation_failure_on_inclusive_minimum_and_inclusive_maximum_overlapping() -> None:
    pass


def test_validation_failure_on_inclusive_minimum_and_exclusive_maximum_overlapping() -> None:
    pass


def test_validation_failure_on_exclusive_minimum_and_inclusive_maximum_overlapping() -> None:
    pass


def test_validation_failure_on_exclusive_minimum_and_exclusive_maximum_overlapping() -> None:
    pass


def test_validation_failure_on_single_match_with_inclusive_minimum_and_inclusive_maximum() -> None:
    pass


def test_validation_failure_on_single_match_with_inclusive_minimum_and_exclusive_maximum() -> None:
    pass


def test_validation_failure_on_single_match_with_exclusive_minimum_and_inclusive_maximum() -> None:
    pass


def test_validation_failure_on_single_match_with_exclusive_minimum_and_exclusive_maximum() -> None:
    pass
