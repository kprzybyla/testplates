from typing import TypeVar

from hypothesis import given
from hypothesis import strategies as st

from testplates.result import Failure
from testplates.validators import union_validator
from testplates.validators.exceptions import InvalidTypeError, ChoiceValidationError

from tests.conftest import st_anything_except

_T = TypeVar("_T")


def test_repr() -> None:
    fmt = "testplates.union_validator()"

    choices = {}
    validator = union_validator(choices)

    assert repr(validator.value) == fmt


def test_success() -> None:
    pass


def test_failure_when_invalid_key_is_passed() -> None:
    pass


@given(data=st_anything_except(tuple))
def test_failure_when_data_type_validation_fails(data: _T) -> None:
    choices = {}
    validator = union_validator(choices)

    assert not validator.is_failure

    result = validator.value(data)

    assert result.is_failure

    error = result.error

    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == (tuple,)


@given(key=st.text())
def test_failure_when_data_field_validation_fails(key: str) -> None:
    value = 0
    failure = Failure(...)
    data = (key, value)

    def validator(v) -> Failure:
        assert v is value
        return failure

    validator = union_validator({key: validator})

    assert not validator.is_failure

    result = validator.value(data)

    assert result.is_failure

    error = result.error

    assert isinstance(error, ChoiceValidationError)
    assert error.data == data
    assert error.key == key
    assert error.error == failure
