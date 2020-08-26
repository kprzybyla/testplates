from typing import Any

from resultful import (
    unwrap_success,
    unwrap_failure,
)

from hypothesis import (
    given,
    strategies as st,
)

from testplates import (
    type_validator,
    InvalidTypeValueError,
    InvalidTypeError,
)

from tests.strategies import (
    st_anything_comparable,
    st_anything_except_classinfo,
    st_anytype_except_type_of,
)


@given(data=st_anything_comparable())
def test_repr(data: Any) -> None:
    assert (validator_result := type_validator(type(data)))

    fmt = "testplates.type_validator({type})"
    validator = unwrap_success(validator_result)
    assert repr(validator) == fmt.format(type=type(data))


@given(data=st_anything_comparable())
def test_success(data: Any) -> None:
    assert (validator_result := type_validator(type(data)))

    validator = unwrap_success(validator_result)
    assert (validation_result := validator(data))

    outcome = unwrap_success(validation_result)
    assert outcome is None


@given(data=st_anything_except_classinfo())
def test_failure_when_type_is_not_a_classinfo(data: Any) -> None:
    assert not (validator_result := type_validator(data))

    error = unwrap_failure(validator_result)
    assert isinstance(error, InvalidTypeValueError)
    assert error.given_type == data


@given(st_data=st.data(), data=st_anything_comparable())
def test_failure_when_data_validation_fails(st_data: st.DataObject, data: Any) -> None:
    any_type_except_data = st_data.draw(st_anytype_except_type_of(data))
    assert (validator_result := type_validator(any_type_except_data))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == (any_type_except_data,)
