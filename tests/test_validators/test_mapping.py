from typing import TypeVar, Mapping, Callable
from dataclasses import dataclass

from hypothesis import given
from hypothesis import strategies as st

# from testplates.base.structure import Structure
from testplates.result import Success, Failure
from testplates.validators import mapping_validator
from testplates.validators.exceptions import (
    InvalidTypeError,
    RequiredKeyMissingError,
    FieldValidationError,
)

from tests.conftest import st_anything_except

_T = TypeVar("_T")


@dataclass
class FakeField:

    name: str
    is_optional: bool
    validator: Callable = None


def create_structure(*fields):
    _fake_fields_ = {field.name: field for field in fields}

    class Structure:

        _fields_ = _fake_fields_

    return Structure()


def test_repr() -> None:
    fmt = "testplates.mapping_validator({structure})"

    structure = create_structure()
    validator = mapping_validator(structure)

    assert repr(validator.value) == fmt.format(structure=structure)


@given(key=st.text())
def test_success(key: str) -> None:
    value = 0
    data = {key: value}

    def validator(v) -> Success[None]:
        assert v is value
        return Success(None)

    field = FakeField(key, is_optional=True, validator=validator)

    structure = create_structure(field)
    validator = mapping_validator(structure)

    assert not validator.is_failure

    result = validator.value(data)

    assert not result.is_failure


@given(key=st.text())
def test_success_with_optional_field(key: str) -> None:
    data = {}
    field = FakeField(key, is_optional=True)

    structure = create_structure(field)
    validator = mapping_validator(structure)

    assert not validator.is_failure

    result = validator.value(data)

    assert not result.is_failure


@given(data=st_anything_except(Mapping))
def test_failure_when_data_type_validation_fails(data: _T) -> None:
    structure = create_structure()
    validator = mapping_validator(structure)

    assert not validator.is_failure

    result = validator.value(data)

    assert result.is_failure

    error = result.error

    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == (Mapping,)


@given(key=st.text())
def test_failure_when_data_required_key_is_missing(key: str) -> None:
    data = {}
    field = FakeField(key, is_optional=False)

    structure = create_structure(field)
    validator = mapping_validator(structure)

    assert not validator.is_failure

    result = validator.value(data)

    assert result.is_failure

    error = result.error

    assert isinstance(error, RequiredKeyMissingError)
    assert error.data == data
    assert error.field == field


@given(key=st.text())
def test_failure_when_data_field_validation_fails(key: str) -> None:
    value = 0
    failure = Failure(...)
    data = {key: value}

    def validator(v) -> Failure[Exception]:
        assert v is value
        return failure

    field = FakeField(key, is_optional=True, validator=validator)

    structure = create_structure(field)
    validator = mapping_validator(structure)

    assert not validator.is_failure

    result = validator.value(data)

    assert result.is_failure

    error = result.error

    assert isinstance(error, FieldValidationError)
    assert error.data == data
    assert error.key == key
    assert error.error == failure
