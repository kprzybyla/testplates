import pytest

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
from .conftest import anything, template_parameters, template_and_storage_parameters


@given(value=anything())
@template_and_storage_parameters
def test_equality(value: int, template_type: TemplateType, storage_type: StorageType) -> None:
    class Template(template_type):  # type: ignore

        key: Required[int] = field()

    assert Template(key=value) == storage_type(key=value)


@given(value=anything())
@template_and_storage_parameters
def test_inequality_due_to_unequal_key(
    value: int, template_type: TemplateType, storage_type: StorageType
) -> None:
    class Template(template_type):  # type: ignore

        key: Required[int] = field()

    assert Template(key=value) != storage_type(other=value)


@given(value=anything(), other=anything())
@template_and_storage_parameters
def test_inequality_due_to_unequal_value(
    value: int, other: int, template_type: TemplateType, storage_type: StorageType
) -> None:
    assume(value != other)

    class Template(template_type):  # type: ignore

        key: Required[int] = field()

    assert Template(key=value) != storage_type(key=other)


@given(value=anything())
@template_and_storage_parameters
def test_default_value(value: int, template_type: TemplateType, storage_type: StorageType) -> None:
    class Template(template_type):  # type: ignore

        key: Required[int] = field(default=value)

    assert Template() == storage_type(key=value)


@given(value=anything(), default=anything())
@template_and_storage_parameters
def test_default_value_override(
    value: int, default: int, template_type: TemplateType, storage_type: StorageType
) -> None:
    assume(value != default)

    class Template(template_type):  # type: ignore

        key: Required[int] = field(default=default)

    assert Template(key=value) == storage_type(key=value)


@given(value=anything())
@template_and_storage_parameters
def test_any_value_matches_anything_in_required_field(
    value: int, template_type: TemplateType, storage_type: StorageType
) -> None:
    class Template(template_type):  # type: ignore

        key: Required[int] = field()

    assert Template(key=ANY) == storage_type(key=value)


@given(value=anything())
@template_and_storage_parameters
def test_any_value_matches_anything_in_optional_field(
    value: int, template_type: TemplateType, storage_type: StorageType
) -> None:
    class Template(template_type):  # type: ignore

        key: Optional[int] = field(optional=True)

    assert Template(key=ANY) == storage_type(key=value)


@given(value=anything())
@template_and_storage_parameters
def test_wildcard_value_matches_anything_in_optional_field(
    value: int, template_type: TemplateType, storage_type: StorageType
) -> None:
    class Template(template_type):  # type: ignore

        key: Optional[int] = field(optional=True)

    assert Template(key=WILDCARD) == storage_type()
    assert Template(key=WILDCARD) == storage_type(key=value)


@template_parameters
def test_wildcard_value_raises_value_error_in_required_field(template_type: TemplateType) -> None:
    class Template(template_type):  # type: ignore

        key: Required[int] = field()

    with pytest.raises(ValueError):
        Template(key=WILDCARD)

    with pytest.raises(ProhibitedValueError):
        Template(key=WILDCARD)


@template_and_storage_parameters
def test_absent_value_matches_anything_in_optional_field(
    template_type: TemplateType, storage_type: StorageType
) -> None:
    class Template(template_type):  # type: ignore

        key: Optional[int] = field(optional=True)

    assert Template(key=ABSENT) == storage_type()


@given(value=anything())
@template_and_storage_parameters
def test_absent_value_mismatches_any_value_in_optional_field(
    value: int, template_type: TemplateType, storage_type: StorageType
) -> None:
    class Template(template_type):  # type: ignore

        key: Optional[int] = field(optional=True)

    assert Template(key=ABSENT) != storage_type(key=value)


@template_parameters
def test_absent_value_raises_value_error_in_required_field(template_type: TemplateType) -> None:
    class Template(template_type):  # type: ignore

        key: Required[int] = field()

    with pytest.raises(ValueError):
        Template(key=ABSENT)

    with pytest.raises(ProhibitedValueError):
        Template(key=ABSENT)


@given(value=anything())
@template_parameters
def test_unexpected_value_raises_value_error(value: int, template_type: TemplateType) -> None:
    class Template(template_type):  # type: ignore
        pass

    with pytest.raises(ValueError):
        Template(key=value)

    with pytest.raises(UnexpectedValueError):
        Template(key=value)


@template_parameters
def test_missing_value_in_required_field_raises_value_error(template_type: TemplateType) -> None:
    class Template(template_type):  # type: ignore

        key: Required[int] = field()

    with pytest.raises(ValueError):
        Template()

    with pytest.raises(MissingValueError):
        Template()


@template_parameters
def test_missing_value_in_optional_field_raises_value_error(template_type: TemplateType) -> None:
    class Template(template_type):  # type: ignore

        key: Optional[int] = field(optional=True)

    with pytest.raises(ValueError):
        Template()

    with pytest.raises(MissingValueError):
        Template()


@given(default=anything())
@template_parameters
def test_default_value_prevents_value_error_in_required_field_on_missing_value(
    default: int, template_type: TemplateType
) -> None:
    class Template(template_type):  # type: ignore

        key: Required[int] = field(default=default)

    Template()


@given(default=anything())
@template_parameters
def test_default_value_prevents_value_error_in_optional_field_on_missing_value(
    default: int, template_type: TemplateType
) -> None:
    class Template(template_type):  # type: ignore

        key: Optional[int] = field(default=default, optional=True)

    Template()
