from typing import TypeVar

from hypothesis import given, strategies as st

from testplates.validators import type_validator
from testplates.validators.exceptions import InvalidTypeError

from tests.conftest import st_anything_comparable, st_anytype_except_type_of

_T = TypeVar("_T")


@given(data=st_anything_comparable())
def test_validation_success(data: _T) -> None:
    validate = type_validator(allowed_types=type(data))
    error = validate(data)

    assert error is None


@given(st_data=st.data(), data=st_anything_comparable())
def test_validation_failure(st_data: st.DataObject, data: _T) -> None:
    any_type_except_data = st_data.draw(st_anytype_except_type_of(data))

    validate = type_validator(allowed_types=any_type_except_data)
    error = validate(data)

    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == any_type_except_data
