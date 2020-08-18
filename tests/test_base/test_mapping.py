from typing import Any, TypeVar, Final

from hypothesis import given

from testplates import field, Mapping, Required, Optional

from tests.strategies import st_anything_comparable

_T = TypeVar("_T")

KEY: Final[str] = "key"


def test_create() -> None:
    raise NotImplementedError()


@given(value=st_anything_comparable())
def test_value_access_in_required_field(value: _T) -> None:
    class Template(Mapping[Any]):

        key: Required[_T] = field()

    template = Template(key=value)

    assert template[KEY] == value


@given(value=st_anything_comparable(), default=st_anything_comparable())
def test_value_access_in_required_field_with_default_value(value: _T, default: _T) -> None:
    class Template(Mapping[Any]):

        key: Required[_T] = field(default=default)

    template_value = Template(key=value)
    template_default = Template()

    assert template_value[KEY] == value
    assert template_default[KEY] == default


@given(value=st_anything_comparable())
def test_value_access_in_optional_field(value: _T) -> None:
    class Template(Mapping[Any]):

        key: Optional[_T] = field(optional=True)

    template = Template(key=value)

    assert template[KEY] == value


@given(value=st_anything_comparable(), default=st_anything_comparable())
def test_value_access_in_optional_field_with_default_value(value: _T, default: _T) -> None:
    class Template(Mapping[Any]):

        key: Optional[_T] = field(default=default, optional=True)

    template_value = Template(key=value)
    template_default = Template()

    assert template_value[KEY] == value
    assert template_default[KEY] == default


@given(value=st_anything_comparable())
def test_len(value: _T) -> None:
    class Template(Mapping[Any]):

        key: Required[_T] = field()

    template = Template(key=value)

    assert len(template) == 1


@given(value=st_anything_comparable())
def test_iter(value: _T) -> None:
    class Template(Mapping[Any]):

        key: Required[_T] = field()

    template = Template(key=value)

    assert list(iter(template)) == [KEY]
