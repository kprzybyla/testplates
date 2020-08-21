from string import printable

from resultful import unwrap_success, unwrap_failure
from hypothesis import given, assume
from hypothesis import strategies as st

from testplates import ANY, WILDCARD, ABSENT
from testplates import initialize, fields, field
from testplates import MissingValueError, UnexpectedValueError, ProhibitedValueError

from tests.strategies import Draw

from .assets import CreateFunctionType, StorageType
from .conftest import create_function_parameters, create_function_and_storage_type_parameters


@st.composite
def st_name(draw: Draw[str]) -> str:
    return draw(st.text(printable))


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st.integers())
@create_function_parameters
def test_repr(name: str, key: str, value: int, create_function: CreateFunctionType) -> None:
    assert (field_result := field(int))

    template_type = create_function(name, **{key: field_result})
    assert (result := initialize(template_type(), **{key: value}))

    template = unwrap_success(result)
    repr_format = f"{name}({key}={value!r})"
    assert repr(template) == repr_format


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st.integers())
@create_function_parameters
def test_meta_repr(name: str, key: str, value: int, create_function: CreateFunctionType) -> None:
    assert (field_result := field(int))

    template_type = create_function(name, **{key: field_result})
    assert (result := initialize(template_type(), **{key: value}))

    template = unwrap_success(result)
    field_object = unwrap_success(field_result)
    repr_format = f"testplates.StructureMeta({key}={field_object!r})"
    assert repr(template_type) == repr(type(template)) == repr_format


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st.integers())
@create_function_and_storage_type_parameters
def test_equality(
    name: str,
    key: str,
    value: int,
    create_function: CreateFunctionType,
    storage_type: StorageType,
) -> None:
    assert (field_result := field(int))

    template_type = create_function(name, **{key: field_result})
    assert (result := initialize(template_type(), **{key: value}))

    template = unwrap_success(result)
    assert template == storage_type(**{key: value})


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), other_key=st.text(), value=st.integers())
@create_function_and_storage_type_parameters
def test_inequality_due_to_unequal_key(
    name: str,
    key: str,
    other_key: str,
    value: int,
    create_function: CreateFunctionType,
    storage_type: StorageType,
) -> None:
    assume(key != other_key)

    assert (field_result := field(int))

    template_type = create_function(name, **{key: field_result})
    assert (result := initialize(template_type(), **{key: value}))

    template = unwrap_success(result)
    assert template != storage_type(**{other_key: value})


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st.integers(), other_value=st.integers())
@create_function_and_storage_type_parameters
def test_inequality_due_to_unequal_value(
    name: str,
    key: str,
    value: int,
    other_value: int,
    create_function: CreateFunctionType,
    storage_type: StorageType,
) -> None:
    assume(value != other_value)

    assert (field_result := field(int))

    template_type = create_function(name, **{key: field_result})
    assert (result := initialize(template_type(), **{key: value}))

    template = unwrap_success(result)
    assert template != storage_type(**{key: other_value})


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st.integers())
@create_function_and_storage_type_parameters
def test_default_value(
    name: str,
    key: str,
    value: int,
    create_function: CreateFunctionType,
    storage_type: StorageType,
) -> None:
    assert (field_result := field(int, default=value))

    template_type = create_function(name, **{key: field_result})
    assert (result := initialize(template_type(), **{key: value}))

    template = unwrap_success(result)
    assert template == storage_type(**{key: value})


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st.integers(), default=st.integers())
@create_function_and_storage_type_parameters
def test_default_value_override(
    name: str,
    key: str,
    value: int,
    default: int,
    create_function: CreateFunctionType,
    storage_type: StorageType,
) -> None:
    assume(value != default)

    assert (field_result := field(int, default=value))

    template_type = create_function(name, **{key: field_result})
    assert (result := initialize(template_type(), **{key: value}))

    template = unwrap_success(result)
    assert template == storage_type(**{key: value})


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st.integers())
@create_function_and_storage_type_parameters
def test_any_value_matches_anything_in_required_field(
    name: str,
    key: str,
    value: int,
    create_function: CreateFunctionType,
    storage_type: StorageType,
) -> None:
    assert (field_result := field(int))

    template_type = create_function(name, **{key: field_result})
    assert (result := initialize(template_type(), **{key: ANY}))

    template = unwrap_success(result)
    assert template == storage_type(**{key: value})


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st.integers())
@create_function_and_storage_type_parameters
def test_any_value_matches_anything_in_optional_field(
    name: str,
    key: str,
    value: int,
    create_function: CreateFunctionType,
    storage_type: StorageType,
) -> None:
    assert (field_result := field(int, optional=True))

    template_type = create_function(name, **{key: field_result})
    assert (result := initialize(template_type(), **{key: ANY}))

    template = unwrap_success(result)
    assert template == storage_type(**{key: value})


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st.integers())
@create_function_and_storage_type_parameters
def test_wildcard_value_matches_anything_in_optional_field(
    name: str,
    key: str,
    value: int,
    create_function: CreateFunctionType,
    storage_type: StorageType,
) -> None:
    assert (field_result := field(int, optional=True))

    template_type = create_function(name, **{key: field_result})
    assert (result := initialize(template_type(), **{key: WILDCARD}))

    template = unwrap_success(result)
    assert template == storage_type()
    assert template == storage_type(**{key: value})


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text())
@create_function_parameters
def test_wildcard_value_raises_value_error_in_required_field(
    name: str, key: str, create_function: CreateFunctionType
) -> None:
    assert (field_result := field(int))

    template_type = create_function(name, **{key: field_result})
    assert not (result := initialize(template_type(), **{key: WILDCARD}))

    error = unwrap_failure(result)
    field_object = unwrap_success(field_result)
    assert isinstance(error, ProhibitedValueError)
    assert error.field == field_object
    assert error.value == WILDCARD


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text())
@create_function_and_storage_type_parameters
def test_absent_value_matches_anything_in_optional_field(
    name: str, key: str, create_function: CreateFunctionType, storage_type: StorageType,
) -> None:
    assert (field_result := field(int, optional=True))

    template_type = create_function(name, **{key: field_result})
    assert (result := initialize(template_type(), **{key: ABSENT}))

    template = unwrap_success(result)
    assert template == storage_type()


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st.integers())
@create_function_and_storage_type_parameters
def test_absent_value_mismatches_any_value_in_optional_field(
    name: str,
    key: str,
    value: int,
    create_function: CreateFunctionType,
    storage_type: StorageType,
) -> None:
    assert (field_result := field(int, optional=True))

    template_type = create_function(name, **{key: field_result})
    assert (result := initialize(template_type(), **{key: ABSENT}))

    template = unwrap_success(result)
    assert template != storage_type(**{key: value})


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text())
@create_function_parameters
def test_absent_value_raises_value_error_in_required_field(
    name: str, key: str, create_function: CreateFunctionType
) -> None:
    assert (field_result := field(int))

    template_type = create_function(name, **{key: field_result})
    assert not (result := initialize(template_type(), **{key: ABSENT}))

    error = unwrap_failure(result)
    field_object = unwrap_success(field_result)
    assert isinstance(error, ProhibitedValueError)
    assert error.field == field_object
    assert error.value == ABSENT


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st.integers())
@create_function_parameters
def test_unexpected_value_raises_value_error(
    name: str, key: str, value: int, create_function: CreateFunctionType
) -> None:
    template_type = create_function(name)
    assert not (result := initialize(template_type(), **{key: value}))

    error = unwrap_failure(result)
    assert isinstance(error, UnexpectedValueError)
    assert error.key == key
    assert error.value == value


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text())
@create_function_parameters
def test_missing_value_in_required_field_raises_value_error(
    name: str, key: str, create_function: CreateFunctionType
) -> None:
    assert (field_result := field(int))

    template_type = create_function(name, **{key: field_result})
    assert not (result := initialize(template_type()))

    error = unwrap_failure(result)
    field_object = unwrap_success(field_result)
    assert isinstance(error, MissingValueError)
    assert error.field == field_object


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text())
@create_function_parameters
def test_missing_value_in_optional_field_raises_value_error(
    name: str, key: str, create_function: CreateFunctionType
) -> None:
    assert (field_result := field(int, optional=True))

    template_type = create_function(name, **{key: field_result})
    assert not (result := initialize(template_type()))

    error = unwrap_failure(result)
    field_object = unwrap_success(field_result)
    assert isinstance(error, MissingValueError)
    assert error.field == field_object


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), default=st.integers())
@create_function_parameters
def test_default_value_prevents_value_error_in_required_field_on_missing_value(
    name: str, key: str, default: int, create_function: CreateFunctionType
) -> None:
    assert (field_result := field(int, default=default))

    template_type = create_function(name, **{key: field_result})
    assert initialize(template_type())


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), default=st.integers())
@create_function_parameters
def test_default_value_prevents_value_error_in_optional_field_on_missing_value(
    name: str, key: str, default: int, create_function: CreateFunctionType
) -> None:
    assert (field_result := field(int, default=default, optional=True))

    template_type = create_function(name, **{key: field_result})
    assert initialize(template_type())


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), default=st.integers())
@create_function_parameters
def test_required_field_properties_access(
    name: str, key: str, default: int, create_function: CreateFunctionType
) -> None:
    assert (field_result := field(int, default=default))

    template_type = create_function(name, **{key: field_result})
    assert (result := fields(template_type))

    template_fields = unwrap_success(result)
    assert template_fields[key].name == key
    assert template_fields[key].default == default
    assert template_fields[key].is_optional is False


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), default=st.integers())
@create_function_parameters
def test_optional_field_properties_access(
    name: str, key: str, default: int, create_function: CreateFunctionType
) -> None:
    assert (field_result := field(int, default=default, optional=True))

    template_type = create_function(name, **{key: field_result})
    assert (result := fields(template_type))

    template_fields = unwrap_success(result)
    assert template_fields[key].name == key
    assert template_fields[key].default == default
    assert template_fields[key].is_optional is True
