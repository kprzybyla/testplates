from typing import Final

from resultful import unwrap_success, unwrap_failure
from hypothesis import given, assume
from hypothesis import strategies as st

from testplates import ANY, WILDCARD, ABSENT
from testplates import field, Required, Optional
from testplates import MissingValueError, UnexpectedValueError, ProhibitedValueError

from .assets import TemplateType, StorageType
from .conftest import template_parameters, template_and_storage_parameters

KEY: Final[str] = "key"


@given(value=st.integers())
@template_parameters
def test_repr(value: int, template_type: TemplateType[int]) -> None:
    class Template(template_type):  # type: ignore

        key: Required[int] = field(int)

    assert (result := Template()._init_(key=value))

    fmt = "Template({key}={value})"
    template = unwrap_success(result)
    assert repr(template) == fmt.format(key=KEY, value=repr(value))


@given(value=st.integers())
@template_parameters
def test_meta_repr(value: int, template_type: TemplateType[int]) -> None:
    fmt = "testplates.StructureMeta({key}={field})"

    class Template(template_type):  # type: ignore

        key: Required[int] = field(int)

    assert (result := Template()._init_(key=value))

    template = unwrap_success(result)
    assert repr(type(template)) == fmt.format(key=KEY, field=repr(Template.key))


@given(value=st.integers())
@template_and_storage_parameters
def test_equality(
    value: int, template_type: TemplateType[int], storage_type: StorageType[int]
) -> None:
    class Template(template_type):  # type: ignore

        key: Required[int] = field(int)

    assert (result := Template()._init_(key=value))

    template = unwrap_success(result)
    assert template == storage_type(key=value)


@given(value=st.integers())
@template_and_storage_parameters
def test_inequality_due_to_unequal_key(
    value: int, template_type: TemplateType[int], storage_type: StorageType[int]
) -> None:
    class Template(template_type):  # type: ignore

        key: Required[int] = field(int)

    assert (result := Template()._init_(key=value))

    template = unwrap_success(result)
    assert template != storage_type(other=value)


@given(value=st.integers(), other=st.integers())
@template_and_storage_parameters
def test_inequality_due_to_unequal_value(
    value: int, other: int, template_type: TemplateType[int], storage_type: StorageType[int]
) -> None:
    assume(value != other)

    class Template(template_type):  # type: ignore

        key: Required[int] = field(int)

    assert (result := Template()._init_(key=value))

    template = unwrap_success(result)
    assert template != storage_type(key=other)


@given(value=st.integers())
@template_and_storage_parameters
def test_default_value(
    value: int, template_type: TemplateType[int], storage_type: StorageType[int]
) -> None:
    class Template(template_type):  # type: ignore

        key: Required[int] = field(int, default=value)

    assert (result := Template()._init_(key=value))

    template = unwrap_success(result)
    assert template == storage_type(key=value)


@given(value=st.integers(), default=st.integers())
@template_and_storage_parameters
def test_default_value_override(
    value: int, default: int, template_type: TemplateType[int], storage_type: StorageType[int]
) -> None:
    assume(value != default)

    class Template(template_type):  # type: ignore

        key: Required[int] = field(int, default=default)

    assert (result := Template()._init_(key=value))

    template = unwrap_success(result)
    assert template == storage_type(key=value)


@given(value=st.integers())
@template_and_storage_parameters
def test_any_value_matches_anything_in_required_field(
    value: int, template_type: TemplateType[int], storage_type: StorageType[int]
) -> None:
    class Template(template_type):  # type: ignore

        key: Required[int] = field(int)

    assert (result := Template()._init_(key=ANY))

    template = unwrap_success(result)
    assert template == storage_type(key=value)


@given(value=st.integers())
@template_and_storage_parameters
def test_any_value_matches_anything_in_optional_field(
    value: int, template_type: TemplateType[int], storage_type: StorageType[int]
) -> None:
    class Template(template_type):  # type: ignore

        key: Optional[int] = field(int, optional=True)

    assert (result := Template()._init_(key=ANY))

    template = unwrap_success(result)
    assert template == storage_type(key=value)


@given(value=st.integers())
@template_and_storage_parameters
def test_wildcard_value_matches_anything_in_optional_field(
    value: int, template_type: TemplateType[int], storage_type: StorageType[int]
) -> None:
    class Template(template_type):  # type: ignore

        key: Optional[int] = field(int, optional=True)

    assert (result := Template()._init_(key=WILDCARD))

    template = unwrap_success(result)
    assert template == storage_type()
    assert template == storage_type(key=value)


@template_parameters
def test_wildcard_value_raises_value_error_in_required_field(
    template_type: TemplateType[int],
) -> None:
    class Template(template_type):  # type: ignore

        key: Required[int] = field(int)

    assert not (result := Template()._init_(key=WILDCARD))

    error = unwrap_failure(result)
    assert isinstance(error, ProhibitedValueError)
    assert error.field == Template.key
    assert error.value == WILDCARD


@template_and_storage_parameters
def test_absent_value_matches_anything_in_optional_field(
    template_type: TemplateType[int], storage_type: StorageType[int]
) -> None:
    class Template(template_type):  # type: ignore

        key: Optional[int] = field(int, optional=True)

    assert (result := Template()._init_(key=ABSENT))

    template = unwrap_success(result)
    assert template == storage_type()


@given(value=st.integers())
@template_and_storage_parameters
def test_absent_value_mismatches_any_value_in_optional_field(
    value: int, template_type: TemplateType[int], storage_type: StorageType[int]
) -> None:
    class Template(template_type):  # type: ignore

        key: Optional[int] = field(int, optional=True)

    assert (result := Template()._init_(key=ABSENT))

    template = unwrap_success(result)
    assert template != storage_type(key=value)


@template_parameters
def test_absent_value_raises_value_error_in_required_field(
    template_type: TemplateType[int],
) -> None:
    class Template(template_type):  # type: ignore

        key: Required[int] = field(int)

    assert not (result := Template()._init_(key=ABSENT))

    error = unwrap_failure(result)
    assert isinstance(error, ProhibitedValueError)
    assert error.field == Template.key
    assert error.value == ABSENT


@given(value=st.integers())
@template_parameters
def test_unexpected_value_raises_value_error(value: int, template_type: TemplateType[int]) -> None:
    class Template(template_type):  # type: ignore
        pass

    assert not (result := Template()._init_(key=value))

    error = unwrap_failure(result)
    assert isinstance(error, UnexpectedValueError)
    assert error.key == KEY
    assert error.value == value


@template_parameters
def test_missing_value_in_required_field_raises_value_error(
    template_type: TemplateType[int],
) -> None:
    class Template(template_type):  # type: ignore

        key: Required[int] = field(int)

    assert not (result := Template()._init_())

    error = unwrap_failure(result)
    assert isinstance(error, MissingValueError)
    assert error.field == Template.key


@template_parameters
def test_missing_value_in_optional_field_raises_value_error(
    template_type: TemplateType[int],
) -> None:
    class Template(template_type):  # type: ignore

        key: Optional[int] = field(int, optional=True)

    assert not (result := Template()._init_())

    error = unwrap_failure(result)
    assert isinstance(error, MissingValueError)
    assert error.field == Template.key


@given(default=st.integers())
@template_parameters
def test_default_value_prevents_value_error_in_required_field_on_missing_value(
    default: int, template_type: TemplateType[int]
) -> None:
    class Template(template_type):  # type: ignore

        key: Required[int] = field(int, default=default)

    assert Template()._init_()


@given(default=st.integers())
@template_parameters
def test_default_value_prevents_value_error_in_optional_field_on_missing_value(
    default: int, template_type: TemplateType[int]
) -> None:
    class Template(template_type):  # type: ignore

        key: Optional[int] = field(int, default=default, optional=True)

    assert Template()._init_()


@given(default=st.integers())
@template_parameters
def test_required_field_properties_access(default: int, template_type: TemplateType[int]) -> None:
    class Template(template_type):  # type: ignore

        key: Required[int] = field(int, default=default)

    assert Template.key.name == KEY
    assert Template.key.default == default
    assert Template.key.is_optional is False


@given(default=st.integers())
@template_parameters
def test_optional_field_properties_access(default: int, template_type: TemplateType[int]) -> None:
    class Template(template_type):  # type: ignore

        key: Optional[int] = field(int, default=default, optional=True)

    assert Template.key.name == KEY
    assert Template.key.default == default
    assert Template.key.is_optional is True
