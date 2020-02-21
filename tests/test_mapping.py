from typing import TypeVar
from typing_extensions import Final

from hypothesis import given

from testplates import Mapping, field, Required, Optional

from .conftest import st_anything

_T = TypeVar("_T")

KEY: Final[str] = "key"


@given(value=st_anything())
def test_value_access_in_required_field(value: _T) -> None:
    class Template(Mapping):

        key: Required[_T] = field()

    assert Template(key=value)[KEY] == value


@given(value=st_anything(), default=st_anything())
def test_value_access_in_required_field_with_default_value(value: _T, default: _T) -> None:
    class Template(Mapping):

        key: Required[_T] = field(default=default)

    assert Template()[KEY] == default
    assert Template(key=value)[KEY] == value


@given(value=st_anything())
def test_value_access_in_optional_field(value: _T) -> None:
    class Template(Mapping):

        key: Optional[_T] = field(optional=True)

    assert Template(key=value)[KEY] == value


@given(value=st_anything(), default=st_anything())
def test_value_access_in_optional_field_with_default_value(value: _T, default: _T) -> None:
    class Template(Mapping):

        key: Optional[_T] = field(default=default, optional=True)

    assert Template()[KEY] == default
    assert Template(key=value)[KEY] == value


@given(value=st_anything())
def test_len(value: _T) -> None:
    class Template(Mapping):

        key: Required[_T] = field()

    assert len(Template(key=value)) == 1


@given(value=st_anything())
def test_iter(value: _T) -> None:
    class Template(Mapping):

        key: Required[_T] = field()

    assert list(iter(Template(key=value))) == [KEY]
