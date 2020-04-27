from typing import TypeVar

from hypothesis import given, strategies as st

from testplates.validators import boolean_validator
from testplates.validators.exceptions import InvalidTypeError

from tests.conftest import st_anything_except

_T = TypeVar("_T")


@given(data=st.booleans())
def test_validation_success(data: bool) -> None:
    validate = boolean_validator()
    error = validate(data)

    assert error is None


@given(data=st_anything_except(bool))
def test_validation_failure(data: _T) -> None:
    validate = boolean_validator()
    error = validate(data)

    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == bool
