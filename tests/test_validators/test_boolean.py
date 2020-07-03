from typing import TypeVar

from hypothesis import given, strategies as st

from testplates.validators import boolean_validator
from testplates.validators.exceptions import InvalidTypeError

from tests.conftest import st_anything_except

_T = TypeVar("_T")


def test_repr() -> None:
    fmt = "testplates.boolean_validator()"

    validator = boolean_validator()

    assert repr(validator.value) == fmt


@given(data=st.booleans())
def test_success(data: bool) -> None:
    validator = boolean_validator()

    assert not validator.is_failure

    result = validator.value(data)

    assert not result.is_failure


@given(data=st_anything_except(bool))
def test_failure_when_data_validation_fails(data: _T) -> None:
    validator = boolean_validator()

    assert not validator.is_failure

    result = validator.value(data)

    assert result.is_failure

    error = result.error

    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == (bool,)
