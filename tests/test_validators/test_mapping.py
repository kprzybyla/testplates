from typing import (
    Any,
    Mapping,
)

from resultful import (
    success,
    failure,
    unwrap_success,
    unwrap_failure,
    Result,
)

from hypothesis import (
    given,
    strategies as st,
)

from testplates import (
    field,
    create,
    mapping_validator,
    passthrough_validator,
    FieldType,
    TestplatesError,
    InvalidTypeError,
    RequiredKeyMissingError,
    UnknownFieldError,
    FieldValidationError,
)

from tests.strategies import (
    st_anything_except,
    st_anything_comparable,
)

STRUCTURE_NAME: str = "Structure"


def test_repr() -> None:
    structure_type = create(STRUCTURE_NAME)
    assert (validator_result := mapping_validator(structure_type))

    fmt = "testplates.mapping_validator({structure_type})"
    validator = unwrap_success(validator_result)
    assert repr(validator) == fmt.format(structure_type=structure_type)


@given(key=st.text(), value=st.integers())
def test_success(key: str, value: int) -> None:
    def validator(this_value: Any, /) -> Result[None, TestplatesError]:
        assert this_value == value
        return success(None)

    field_object: FieldType[int] = field(success(validator), optional=True)
    structure_type = create(STRUCTURE_NAME, **{key: field_object})
    assert (validator_result := mapping_validator(structure_type))

    validator = unwrap_success(validator_result)
    assert (validation_result := validator({key: value}))

    outcome = unwrap_success(validation_result)
    assert outcome is None


@given(key=st.text())
def test_success_with_optional_field(key: str) -> None:
    field_object: FieldType[int] = field(passthrough_validator(), optional=True)
    structure_type = create(STRUCTURE_NAME, **{key: field_object})
    assert (validator_result := mapping_validator(structure_type))

    validator = unwrap_success(validator_result)
    assert (validation_result := validator({}))

    outcome = unwrap_success(validation_result)
    assert outcome is None


@given(data=st_anything_except(Mapping))
def test_failure_when_data_type_validation_fails(data: Any) -> None:
    structure_type = create(STRUCTURE_NAME)
    assert (validator_result := mapping_validator(structure_type))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == (Mapping,)


@given(key=st.text())
def test_failure_when_data_required_key_is_missing(key: str) -> None:
    field_object: FieldType[int] = field(passthrough_validator())
    structure_type = create(STRUCTURE_NAME, **{key: field_object})
    assert (validator_result := mapping_validator(structure_type))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator({}))

    error = unwrap_failure(validation_result)
    assert isinstance(error, RequiredKeyMissingError)
    assert error.data == {}
    assert error.field == field_object


@given(key=st.text(), value=st_anything_comparable())
def test_failure_when_data_has_unknown_field(key: str, value: int) -> None:
    structure_type = create(STRUCTURE_NAME)
    assert (validator_result := mapping_validator(structure_type))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator({key: value}))

    error = unwrap_failure(validation_result)
    assert isinstance(error, UnknownFieldError)
    assert error.data == {key: value}
    assert error.structure_type == structure_type


@given(key=st.text(), value=st.integers(), message=st.text())
def test_failure_when_data_field_validation_fails(key: str, value: int, message: str) -> None:
    field_error = TestplatesError(message)

    def validator(this_value: Any, /) -> Result[None, TestplatesError]:
        assert this_value == value
        return failure(field_error)

    field_object: FieldType[int] = field(success(validator), optional=True)
    structure_type = create(STRUCTURE_NAME, **{key: field_object})
    assert (validator_result := mapping_validator(structure_type))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator({key: value}))

    error = unwrap_failure(validation_result)
    assert isinstance(error, FieldValidationError)
    assert error.data == {key: value}
    assert error.field == field_object
    assert error.error == field_error
