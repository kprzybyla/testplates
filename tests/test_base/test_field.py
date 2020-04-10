import pytest

from typing import Any, TypeVar
from hypothesis import given

from testplates import field, Required, Optional, DanglingDescriptorError

from tests.conftest import st_anything_comparable

_T = TypeVar("_T")


def test_repr_for_required_field_without_default_value() -> None:
    fmt = "Field('key', optional=False)"

    class Wrapper:

        key: Required[Any] = field()

    assert repr(Wrapper.key) == fmt.format()


@given(value=st_anything_comparable())
def test_repr_for_required_field_with_default_value(value: _T) -> None:
    fmt = "Field('key', default={value}, optional=False)"

    class Wrapper:

        key: Required[_T] = field(default=value)

    assert repr(Wrapper.key) == fmt.format(value=repr(value))


def test_repr_for_optional_field_without_default_value() -> None:
    fmt = "Field('key', optional=True)"

    class Wrapper:

        key: Optional[Any] = field(optional=True)

    assert repr(Wrapper.key) == fmt.format()


@given(value=st_anything_comparable())
def test_repr_for_optional_field_with_default_value(value: _T) -> None:
    fmt = "Field('key', default={value}, optional=True)"

    class Wrapper:

        key: Required[_T] = field(default=value, optional=True)

    assert repr(Wrapper.key) == fmt.format(value=repr(value))


def test_name_raises_dangling_descriptor_error_when_specified_outside_the_class() -> None:
    key: Required[Any] = field()

    with pytest.raises(DanglingDescriptorError):
        print(key.name)
