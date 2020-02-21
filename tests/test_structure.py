import pytest

from typing import TypeVar
from typing_extensions import Final
from hypothesis import given, assume

from testplates import (
    WILDCARD,
    ANY,
    ABSENT,
    field,
    Required,
    Optional,
    MissingValueError,
    UnexpectedValueError,
    ProhibitedValueError,
)

from .assets import TemplateType, StorageType
from .conftest import st_anything, template_parameters, template_and_storage_parameters

_T = TypeVar("_T")

KEY: Final[str] = "key"


@given(value=st_anything())
@template_and_storage_parameters
def test_equality(value: _T, template_type: TemplateType, storage_type: StorageType) -> None:
    class Template(template_type):  # type: ignore

        key: Required[_T] = field()

    assert Template(key=value) == storage_type(key=value)


@given(value=st_anything())
@template_and_storage_parameters
def test_inequality_due_to_unequal_key(
    value: _T, template_type: TemplateType, storage_type: StorageType
) -> None:
    class Template(template_type):  # type: ignore

        key: Required[_T] = field()

    assert Template(key=value) != storage_type(other=value)


@given(value=st_anything(), other=st_anything())
@template_and_storage_parameters
def test_inequality_due_to_unequal_value(
    value: _T, other: _T, template_type: TemplateType, storage_type: StorageType
) -> None:
    assume(value != other)

    class Template(template_type):  # type: ignore

        key: Required[_T] = field()

    assert Template(key=value) != storage_type(key=other)


@given(value=st_anything())
@template_and_storage_parameters
def test_default_value(value: _T, template_type: TemplateType, storage_type: StorageType) -> None:
    class Template(template_type):  # type: ignore

        key: Required[_T] = field(default=value)

    assert Template() == storage_type(key=value)


@given(value=st_anything(), default=st_anything())
@template_and_storage_parameters
def test_default_value_override(
    value: _T, default: _T, template_type: TemplateType, storage_type: StorageType
) -> None:
    assume(value != default)

    class Template(template_type):  # type: ignore

        key: Required[_T] = field(default=default)

    assert Template(key=value) == storage_type(key=value)


@given(value=st_anything())
@template_and_storage_parameters
def test_any_value_matches_anything_in_required_field(
    value: _T, template_type: TemplateType, storage_type: StorageType
) -> None:
    class Template(template_type):  # type: ignore

        key: Required[_T] = field()

    assert Template(key=ANY) == storage_type(key=value)


@given(value=st_anything())
@template_and_storage_parameters
def test_any_value_matches_anything_in_optional_field(
    value: _T, template_type: TemplateType, storage_type: StorageType
) -> None:
    class Template(template_type):  # type: ignore

        key: Optional[_T] = field(optional=True)

    assert Template(key=ANY) == storage_type(key=value)


@given(value=st_anything())
@template_and_storage_parameters
def test_wildcard_value_matches_anything_in_optional_field(
    value: _T, template_type: TemplateType, storage_type: StorageType
) -> None:
    class Template(template_type):  # type: ignore

        key: Optional[_T] = field(optional=True)

    assert Template(key=WILDCARD) == storage_type()
    assert Template(key=WILDCARD) == storage_type(key=value)


@template_parameters
def test_wildcard_value_raises_value_error_in_required_field(template_type: TemplateType) -> None:
    class Template(template_type):  # type: ignore

        key: Required[_T] = field()

    with pytest.raises(ValueError):
        Template(key=WILDCARD)

    with pytest.raises(ProhibitedValueError):
        Template(key=WILDCARD)


@template_and_storage_parameters
def test_absent_value_matches_anything_in_optional_field(
    template_type: TemplateType, storage_type: StorageType
) -> None:
    class Template(template_type):  # type: ignore

        key: Optional[_T] = field(optional=True)

    assert Template(key=ABSENT) == storage_type()


@given(value=st_anything())
@template_and_storage_parameters
def test_absent_value_mismatches_any_value_in_optional_field(
    value: _T, template_type: TemplateType, storage_type: StorageType
) -> None:
    class Template(template_type):  # type: ignore

        key: Optional[_T] = field(optional=True)

    assert Template(key=ABSENT) != storage_type(key=value)


@template_parameters
def test_absent_value_raises_value_error_in_required_field(template_type: TemplateType) -> None:
    class Template(template_type):  # type: ignore

        key: Required[_T] = field()

    with pytest.raises(ValueError):
        Template(key=ABSENT)

    with pytest.raises(ProhibitedValueError):
        Template(key=ABSENT)


@given(value=st_anything())
@template_parameters
def test_unexpected_value_raises_value_error(value: _T, template_type: TemplateType) -> None:
    class Template(template_type):  # type: ignore
        pass

    with pytest.raises(ValueError):
        Template(key=value)

    with pytest.raises(UnexpectedValueError):
        Template(key=value)


@template_parameters
def test_missing_value_in_required_field_raises_value_error(template_type: TemplateType) -> None:
    class Template(template_type):  # type: ignore

        key: Required[_T] = field()

    with pytest.raises(ValueError):
        Template()

    with pytest.raises(MissingValueError):
        Template()


@template_parameters
def test_missing_value_in_optional_field_raises_value_error(template_type: TemplateType) -> None:
    class Template(template_type):  # type: ignore

        key: Optional[_T] = field(optional=True)

    with pytest.raises(ValueError):
        Template()

    with pytest.raises(MissingValueError):
        Template()


@given(default=st_anything())
@template_parameters
def test_default_value_prevents_value_error_in_required_field_on_missing_value(
    default: _T, template_type: TemplateType
) -> None:
    class Template(template_type):  # type: ignore

        key: Required[_T] = field(default=default)

    Template()


@given(default=st_anything())
@template_parameters
def test_default_value_prevents_value_error_in_optional_field_on_missing_value(
    default: _T, template_type: TemplateType
) -> None:
    class Template(template_type):  # type: ignore

        key: Optional[_T] = field(default=default, optional=True)

    Template()


@given(default=st_anything())
@template_parameters
def test_required_field_properties_access(default: _T, template_type: TemplateType) -> None:
    class Template(template_type):  # type: ignore

        key: Required[_T] = field(default=default)

    assert Template.key.name == KEY
    assert Template.key.default == default
    assert Template.key.is_optional is False


@given(default=st_anything())
@template_parameters
def test_optional_field_properties_access(default: _T, template_type: TemplateType) -> None:
    class Template(template_type):  # type: ignore

        key: Optional[_T] = field(default=default, optional=True)

    assert Template.key.name == KEY
    assert Template.key.default == default
    assert Template.key.is_optional is True
