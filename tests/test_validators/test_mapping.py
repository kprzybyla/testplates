from typing import Any, Type, TypeVar, Mapping

from resultful import success, failure, unwrap_success, unwrap_failure, Result
from hypothesis import given
from hypothesis import strategies as st

from testplates import field, create_object, Object, Required, Optional
from testplates import mapping_validator, passthrough_validator
from testplates import (
    TestplatesError,
    InvalidTypeError,
    RequiredKeyMissingError,
    UnknownFieldError,
    FieldValidationError,
)

from tests.strategies import st_anything_except, st_anything_comparable

_T = TypeVar("_T")

STRUCTURE_NAME: str = "Structure"


# noinspection PyTypeChecker
def test_repr() -> None:
    structure_type: Type[Object[Any]] = create_object(STRUCTURE_NAME)
    assert (validator_result := mapping_validator(structure_type))

    fmt = "testplates.MappingValidator({structure_type})"
    validator = unwrap_success(validator_result)
    assert repr(validator) == fmt.format(structure_type=structure_type)


# noinspection PyTypeChecker
@given(key=st.text(), value=st_anything_comparable())
def test_success(key: str, value: _T) -> None:
    def validator(this_value: Any, /) -> Result[None, TestplatesError]:
        assert this_value == value
        return success(None)

    field_object: Optional[_T] = field(validator, optional=True)
    structure_type = create_object(STRUCTURE_NAME, {key: field_object})
    assert (validator_result := mapping_validator(structure_type))

    validator = unwrap_success(validator_result)
    assert (validation_result := validator({key: value}))

    value = unwrap_success(validation_result)  # type: ignore
    assert value is None


# noinspection PyTypeChecker
@given(key=st.text())
def test_success_with_optional_field(key: str) -> None:
    field_object: Optional[Any] = field(passthrough_validator, optional=True)
    structure_type = create_object(STRUCTURE_NAME, {key: field_object})
    assert (validator_result := mapping_validator(structure_type))

    validator = unwrap_success(validator_result)
    assert (validation_result := validator({}))

    value = unwrap_success(validation_result)
    assert value is None


# noinspection PyTypeChecker
@given(data=st_anything_except(Mapping))
def test_failure_when_data_type_validation_fails(data: Any) -> None:
    structure_type: Type[Object[Any]] = create_object(STRUCTURE_NAME)
    assert (validator_result := mapping_validator(structure_type))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == (Mapping,)


# noinspection PyTypeChecker
@given(key=st.text())
def test_failure_when_data_required_key_is_missing(key: str) -> None:
    field_object: Required[Any] = field(passthrough_validator)
    structure_type = create_object(STRUCTURE_NAME, {key: field_object})
    assert (validator_result := mapping_validator(structure_type))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator({}))

    error = unwrap_failure(validation_result)
    assert isinstance(error, RequiredKeyMissingError)
    assert error.data == {}
    assert error.field == field_object


# noinspection PyTypeChecker
@given(key=st.text(), value=st_anything_comparable())
def test_failure_when_data_has_unknown_field(key: str, value: _T) -> None:
    structure_type: Type[Object[Any]] = create_object(STRUCTURE_NAME, {})
    assert (validator_result := mapping_validator(structure_type))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator({key: value}))

    error = unwrap_failure(validation_result)
    assert isinstance(error, UnknownFieldError)
    assert error.data == {key: value}
    assert error.structure_type == structure_type


# noinspection PyTypeChecker
@given(key=st.text(), value=st_anything_comparable(), message=st.text())
def test_failure_when_data_field_validation_fails(key: str, value: _T, message: str) -> None:
    field_error = TestplatesError(message)

    def validator(this_value: Any, /) -> Result[None, TestplatesError]:
        assert this_value == value
        return failure(field_error)

    field_object: Optional[_T] = field(validator, optional=True)
    structure_type = create_object(STRUCTURE_NAME, {key: field_object})
    assert (validator_result := mapping_validator(structure_type))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator({key: value}))

    error = unwrap_failure(validation_result)
    assert isinstance(error, FieldValidationError)
    assert error.data == {key: value}
    assert error.field == field_object
    assert error.error == field_error
