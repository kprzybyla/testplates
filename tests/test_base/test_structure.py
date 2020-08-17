from typing import Any, TypeVar, Final
from functools import partial

import pytest

from hypothesis import given, assume

from testplates import ANY, WILDCARD, ABSENT
from testplates import field, Required, Optional
from testplates import MissingValueError, UnexpectedValueError, ProhibitedValueError

from tests.strategies import st_anything_comparable

from .assets import TemplateType, StorageType
from .conftest import template_parameters, template_and_storage_parameters

_T = TypeVar("_T")

KEY: Final[str] = "key"


@given(value=st_anything_comparable())
@template_parameters
def test_repr(value: _T, template_type: TemplateType[_T]) -> None:
    fmt = "Template({key}={value})"

    class Template(template_type):  # type: ignore

        key: Required[Any] = field()

    template = Template(key=value)

    assert repr(template) == fmt.format(key=KEY, value=repr(value))


@given(value=st_anything_comparable())
@template_parameters
def test_meta_repr(value: _T, template_type: TemplateType[_T]) -> None:
    fmt = "testplates.StructureMeta({key}={field})"

    class Template(template_type):  # type: ignore

        key: Required[Any] = field()

    template = Template(key=value)

    assert repr(type(template)) == fmt.format(key=KEY, field=repr(Template.key))


@given(value=st_anything_comparable())
@template_and_storage_parameters
def test_equality(
    value: _T, template_type: TemplateType[_T], storage_type: StorageType[_T]
) -> None:
    class Template(template_type):  # type: ignore

        key: Required[_T] = field()

    template = Template(key=value)

    assert template == storage_type(key=value)


@given(value=st_anything_comparable())
@template_and_storage_parameters
def test_inequality_due_to_unequal_key(
    value: _T, template_type: TemplateType[_T], storage_type: StorageType[_T]
) -> None:
    class Template(template_type):  # type: ignore

        key: Required[_T] = field()

    template = Template(key=value)

    assert template != storage_type(other=value)


@given(value=st_anything_comparable(), other=st_anything_comparable())
@template_and_storage_parameters
def test_inequality_due_to_unequal_value(
    value: _T, other: _T, template_type: TemplateType[_T], storage_type: StorageType[_T]
) -> None:
    assume(value != other)

    class Template(template_type):  # type: ignore

        key: Required[_T] = field()

    template = Template(key=value)

    assert template != storage_type(key=other)


@given(value=st_anything_comparable())
@template_and_storage_parameters
def test_default_value(
    value: _T, template_type: TemplateType[_T], storage_type: StorageType[_T]
) -> None:
    class Template(template_type):  # type: ignore

        key: Required[_T] = field(default=value)

    template = Template()

    assert template == storage_type(key=value)


@given(value=st_anything_comparable(), default=st_anything_comparable())
@template_and_storage_parameters
def test_default_value_override(
    value: _T, default: _T, template_type: TemplateType[_T], storage_type: StorageType[_T]
) -> None:
    assume(value != default)

    class Template(template_type):  # type: ignore

        key: Required[_T] = field(default=default)

    template = Template(key=value)

    assert template == storage_type(key=value)


@given(value=st_anything_comparable())
@template_and_storage_parameters
def test_any_value_matches_anything_in_required_field(
    value: _T, template_type: TemplateType[_T], storage_type: StorageType[_T]
) -> None:
    class Template(template_type):  # type: ignore

        key: Required[_T] = field()

    template = Template(key=ANY)

    assert template == storage_type(key=value)


@given(value=st_anything_comparable())
@template_and_storage_parameters
def test_any_value_matches_anything_in_optional_field(
    value: _T, template_type: TemplateType[_T], storage_type: StorageType[_T]
) -> None:
    class Template(template_type):  # type: ignore

        key: Optional[_T] = field(optional=True)

    template = Template(key=ANY)

    assert template == storage_type(key=value)


@given(value=st_anything_comparable())
@template_and_storage_parameters
def test_wildcard_value_matches_anything_in_optional_field(
    value: _T, template_type: TemplateType[_T], storage_type: StorageType[_T]
) -> None:
    class Template(template_type):  # type: ignore

        key: Optional[_T] = field(optional=True)

    template = Template(key=WILDCARD)

    assert template == storage_type()
    assert template == storage_type(key=value)


@template_parameters
def test_wildcard_value_raises_value_error_in_required_field(
    template_type: TemplateType[_T],
) -> None:
    class Template(template_type):  # type: ignore

        key: Required[Any] = field()

    template_partial = partial(Template, key=WILDCARD)

    with pytest.raises(ProhibitedValueError) as exception:
        template_partial()

    assert exception.value.field == Template.key
    assert exception.value.value == WILDCARD


@template_and_storage_parameters
def test_absent_value_matches_anything_in_optional_field(
    template_type: TemplateType[_T], storage_type: StorageType[_T]
) -> None:
    class Template(template_type):  # type: ignore

        key: Optional[Any] = field(optional=True)

    template = Template(key=ABSENT)

    assert template == storage_type()


@given(value=st_anything_comparable())
@template_and_storage_parameters
def test_absent_value_mismatches_any_value_in_optional_field(
    value: _T, template_type: TemplateType[_T], storage_type: StorageType[_T]
) -> None:
    class Template(template_type):  # type: ignore

        key: Optional[_T] = field(optional=True)

    template = Template(key=ABSENT)

    assert template != storage_type(key=value)


@template_parameters
def test_absent_value_raises_value_error_in_required_field(
    template_type: TemplateType[_T],
) -> None:
    class Template(template_type):  # type: ignore

        key: Required[Any] = field()

    template_partial = partial(Template, key=ABSENT)

    with pytest.raises(ProhibitedValueError) as exception:
        template_partial()

    assert exception.value.field == Template.key
    assert exception.value.value == ABSENT


@given(value=st_anything_comparable())
@template_parameters
def test_unexpected_value_raises_value_error(value: _T, template_type: TemplateType[_T]) -> None:
    class Template(template_type):  # type: ignore
        pass

    template_partial = partial(Template, key=value)

    with pytest.raises(UnexpectedValueError) as exception:
        template_partial()

    assert exception.value.key == KEY
    assert exception.value.value == value


@template_parameters
def test_missing_value_in_required_field_raises_value_error(
    template_type: TemplateType[_T],
) -> None:
    class Template(template_type):  # type: ignore

        key: Required[Any] = field()

    template_partial = partial(Template)

    with pytest.raises(MissingValueError) as exception:
        template_partial()

    assert exception.value.field == Template.key


@template_parameters
def test_missing_value_in_optional_field_raises_value_error(
    template_type: TemplateType[_T],
) -> None:
    class Template(template_type):  # type: ignore

        key: Optional[Any] = field(optional=True)

    template_partial = partial(Template)

    with pytest.raises(MissingValueError) as exception:
        template_partial()

    assert exception.value.field == Template.key


@given(default=st_anything_comparable())
@template_parameters
def test_default_value_prevents_value_error_in_required_field_on_missing_value(
    default: _T, template_type: TemplateType[_T]
) -> None:
    class Template(template_type):  # type: ignore

        key: Required[_T] = field(default=default)

    Template()


@given(default=st_anything_comparable())
@template_parameters
def test_default_value_prevents_value_error_in_optional_field_on_missing_value(
    default: _T, template_type: TemplateType[_T]
) -> None:
    class Template(template_type):  # type: ignore

        key: Optional[_T] = field(default=default, optional=True)

    Template()


@given(default=st_anything_comparable())
@template_parameters
def test_required_field_properties_access(default: _T, template_type: TemplateType[_T]) -> None:
    class Template(template_type):  # type: ignore

        key: Required[Any] = field(default=default)

    assert Template.key.name == KEY
    assert Template.key.default == default
    assert Template.key.is_optional is False


@given(default=st_anything_comparable())
@template_parameters
def test_optional_field_properties_access(default: _T, template_type: TemplateType[_T]) -> None:
    class Template(template_type):  # type: ignore

        key: Optional[Any] = field(default=default, optional=True)

    assert Template.key.name == KEY
    assert Template.key.default == default
    assert Template.key.is_optional is True
