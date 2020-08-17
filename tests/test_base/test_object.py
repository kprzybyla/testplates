from typing import Any, TypeVar

from hypothesis import given

from testplates import field, Object, Required, Optional

from tests.strategies import st_anything_comparable

_T = TypeVar("_T")


@given(value=st_anything_comparable())
def test_value_access_in_required_field(value: _T) -> None:
    class Template(Object[Any]):

        key: Required[_T] = field()

    template = Template(key=value)

    assert template.key == value


@given(value=st_anything_comparable(), default=st_anything_comparable())
def test_value_access_in_required_field_with_default_value(value: _T, default: _T) -> None:
    class Template(Object[Any]):

        key: Required[_T] = field(default=default)

    template_value = Template(key=value)
    template_default = Template()

    assert template_value.key == value
    assert template_default.key == default


@given(value=st_anything_comparable())
def test_value_access_in_optional_field(value: _T) -> None:
    class Template(Object[Any]):

        key: Optional[_T] = field(optional=True)

    template = Template(key=value)

    assert template.key == value


@given(value=st_anything_comparable(), default=st_anything_comparable())
def test_value_access_in_optional_field_with_default_value(value: _T, default: _T) -> None:
    class Template(Object[Any]):

        key: Optional[_T] = field(default=default, optional=True)

    template_value = Template(key=value)
    template_default = Template()

    assert template_value.key == value
    assert template_default.key == default
