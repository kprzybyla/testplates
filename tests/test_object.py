from typing import TypeVar
from hypothesis import given

from testplates import field, Object, Required, Optional

from .conftest import anything

_T = TypeVar("_T")


@given(value=anything())
def test_value_access_in_required_field(value: _T) -> None:
    class Template(Object):

        key: Required[_T] = field()

    assert Template(key=value).key == value


@given(value=anything(), default=anything())
def test_value_access_in_required_field_with_default_value(value: _T, default: _T) -> None:
    class Template(Object):

        key: Required[_T] = field(default=default)

    assert Template().key == default
    assert Template(key=value).key == value


@given(value=anything())
def test_value_access_in_optional_field(value: _T) -> None:
    class Template(Object):

        key: Optional[_T] = field(optional=True)

    assert Template(key=value).key == value


@given(value=anything(), default=anything())
def test_value_access_in_optional_field_with_default_value(value: _T, default: _T) -> None:
    class Template(Object):

        key: Optional[_T] = field(default=default, optional=True)

    assert Template().key == default
    assert Template(key=value).key == value
