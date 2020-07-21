from typing import Any, Mapping

from hypothesis import given
from hypothesis import strategies as st

from testplates import success, failure, unwrap_success, unwrap_failure, Result
from testplates import field, create_object
from testplates import (
    mapping_validator,
    passthrough_validator,
    ValidationError,
    InvalidTypeError,
    RequiredKeyMissingError,
    FieldValidationError,
)

from tests.conftest import st_anything_except, st_anything_comparable

STRUCTURE_NAME: str = "Structure"


def test_repr() -> None:
    fmt = "testplates.MappingValidator({structure})"

    structure = create_object(STRUCTURE_NAME)

    validator_result = mapping_validator(structure)
    validator = unwrap_success(validator_result)

    assert repr(validator) == fmt.format(structure=structure)


@given(key=st.text(), value=st_anything_comparable())
def test_success(key: str, value: Any) -> None:
    data = {key: value}

    def validator(this_value: Any) -> Result[None, ValidationError]:
        assert this_value == value
        return success(None)

    field_object = field(validator, optional=True)
    structure = create_object(STRUCTURE_NAME, {key: field_object})

    validator_result = mapping_validator(structure)
    validator = unwrap_success(validator_result)

    validation_result = validator(data)
    value = unwrap_success(validation_result)

    assert value is None


@given(key=st.text())
def test_success_with_optional_field(key: str) -> None:
    data = {}

    field_object = field(passthrough_validator, optional=True)
    structure = create_object(STRUCTURE_NAME, {key: field_object})

    validator_result = mapping_validator(structure)
    validator = unwrap_success(validator_result)

    validation_result = validator(data)
    value = unwrap_success(validation_result)

    assert value is None


@given(data=st_anything_except(Mapping))
def test_failure_when_data_type_validation_fails(data: Any) -> None:
    structure = create_object(STRUCTURE_NAME)

    validator_result = mapping_validator(structure)
    validator = unwrap_success(validator_result)

    validation_result = validator(data)
    error = unwrap_failure(validation_result)

    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == (Mapping,)


@given(key=st.text())
def test_failure_when_data_required_key_is_missing(key: str) -> None:
    data = {}

    field_object = field(passthrough_validator)
    structure = create_object(STRUCTURE_NAME, {key: field_object})

    validator_result = mapping_validator(structure)
    validator = unwrap_success(validator_result)

    validation_result = validator(data)
    error = unwrap_failure(validation_result)

    assert isinstance(error, RequiredKeyMissingError)
    assert error.data == data
    assert error.field == field_object


# noinspection PyTypeChecker
@given(key=st.text(), value=st_anything_comparable(), message=st.text())
def test_failure_when_data_field_validation_fails(key: str, value: Any, message: str) -> None:
    failure_object = failure(ValidationError(message))

    # noinspection PyTypeChecker
    def validator(this_value: Any) -> Result[None, ValidationError]:
        assert this_value == value
        return failure_object

    field_object = field(validator, optional=True)
    structure = create_object(STRUCTURE_NAME, {key: field_object})

    validator_result = mapping_validator(structure)
    validator = unwrap_success(validator_result)

    data = {key: value}

    validation_result = validator(data)
    error = unwrap_failure(validation_result)

    assert isinstance(error, FieldValidationError)
    assert error.data == data
    assert error.key == key
    assert error.error == failure_object
