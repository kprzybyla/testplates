from typing import Any, Mapping

from hypothesis import given
from hypothesis import strategies as st

from testplates.base.structure import create_structure, Field
from testplates.result import Success, Failure
from testplates.validators import mapping_validator, passthrough_validator
from testplates.validators.exceptions import (
    ValidationError,
    InvalidTypeError,
    RequiredKeyMissingError,
    FieldValidationError,
)

from tests.conftest import st_anything_except, st_anything_comparable


def test_repr() -> None:
    fmt = "testplates.mapping_validator({structure})"

    structure = create_structure("Structure")

    validator_result = mapping_validator(structure)
    validator = Success.get_value(validator_result)

    assert repr(validator) == fmt.format(structure=structure)


@given(key=st.text(), value=st_anything_comparable())
def test_success(key: str, value: Any) -> None:
    data = {key: value}

    def validator(this_value: Any) -> Success[None]:
        assert this_value == value
        return Success(None)

    field = Field(validator, optional=True)
    structure = create_structure("Structure", {key: field})

    validator_result = mapping_validator(structure)
    validator = Success.get_value(validator_result)

    validation_result = validator(data)
    value = Success.get_value(validation_result)

    assert value is None


@given(key=st.text())
def test_success_with_optional_field(key: str) -> None:
    data = {}

    field = Field(passthrough_validator, optional=True)
    structure = create_structure("Structure", {key: field})

    validator_result = mapping_validator(structure)
    validator = Success.get_value(validator_result)

    validation_result = validator(data)
    value = Success.get_value(validation_result)

    assert value is None


@given(data=st_anything_except(Mapping))
def test_failure_when_data_type_validation_fails(data: Any) -> None:
    structure = create_structure("Structure")

    validator_result = mapping_validator(structure)
    validator = Success.get_value(validator_result)

    validation_result = validator(data)
    error = Failure.get_error(validation_result)

    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == (Mapping,)


@given(key=st.text())
def test_failure_when_data_required_key_is_missing(key: str) -> None:
    data = {}

    field = Field(passthrough_validator)
    structure = create_structure("Structure", {key: field})

    validator_result = mapping_validator(structure)
    validator = Success.get_value(validator_result)

    validation_result = validator(data)
    error = Failure.get_error(validation_result)

    assert isinstance(error, RequiredKeyMissingError)
    assert error.data == data
    assert error.field == field


# noinspection PyTypeChecker
@given(key=st.text(), value=st_anything_comparable(), message=st.text())
def test_failure_when_data_field_validation_fails(key: str, value: Any, message: str) -> None:
    failure = Failure(ValidationError(message))

    def validator(this_value: Any) -> Failure[Exception]:
        assert this_value == value
        return failure

    field = Field(validator, optional=True)
    structure = create_structure("Structure", {key: field})

    validator_result = mapping_validator(structure)
    validator = Success.get_value(validator_result)

    data = {key: value}

    validation_result = validator(data)
    error = Failure.get_error(validation_result)

    assert isinstance(error, FieldValidationError)
    assert error.data == data
    assert error.key == key
    assert error.error == failure
