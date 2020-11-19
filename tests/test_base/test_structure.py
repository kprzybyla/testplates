from typing import (
    Any,
    Tuple,
    Dict,
    Iterator,
)

from string import (
    printable,
)

from resultful import (
    failure,
    unwrap_success,
    unwrap_failure,
)

from hypothesis import (
    given,
    assume,
    strategies as st,
)

from testplates import (
    create,
    init,
    modify,
    value_of,
    fields,
    items,
    field,
    Maybe,
    FieldType,
    ANY,
    WILDCARD,
    ABSENT,
    TestplatesError,
    MissingValueError,
    UnexpectedValueError,
    ProhibitedValueError,
    InvalidStructureError,
)

from tests.strategies import Draw


class Storage(Dict[str, Any]):
    pass


@st.composite
def st_name(draw: Draw[str]) -> str:
    return draw(st.text(printable))


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st.integers())
def test_repr(name: str, key: str, value: int) -> None:
    field_object: FieldType[int] = field()
    template_type = create(name, **{key: field_object})
    assert (result := init(template_type, **{key: value}))

    template = unwrap_success(result)
    repr_format = f"{name}({key}={value!r})"
    assert repr(template) == repr_format


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st.integers())
def test_meta_repr(name: str, key: str, value: int) -> None:
    field_object: FieldType[int] = field()
    template_type = create(name, **{key: field_object})
    assert (result := init(template_type, **{key: value}))

    template = unwrap_success(result)
    repr_format = f"testplates.StructureMeta({key}={field_object!r})"
    assert repr(template_type) == repr(type(template)) == repr_format


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st.integers())
def test_equality(
    name: str,
    key: str,
    value: int,
) -> None:
    field_object: FieldType[int] = field()
    template_type = create(name, **{key: field_object})
    assert (result := init(template_type, **{key: value}))

    template = unwrap_success(result)
    assert template == Storage(**{key: value})


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), other_key=st.text(), value=st.integers())
def test_inequality_due_to_unequal_key(
    name: str,
    key: str,
    other_key: str,
    value: int,
) -> None:
    assume(key != other_key)

    field_object: FieldType[int] = field()
    template_type = create(name, **{key: field_object})
    assert (result := init(template_type, **{key: value}))

    template = unwrap_success(result)
    assert template != Storage(**{other_key: value})


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st.integers(), other_value=st.integers())
def test_inequality_due_to_unequal_value(
    name: str,
    key: str,
    value: int,
    other_value: int,
) -> None:
    assume(value != other_value)

    field_object: FieldType[int] = field()
    template_type = create(name, **{key: field_object})
    assert (result := init(template_type, **{key: value}))

    template = unwrap_success(result)
    assert template != Storage(**{key: other_value})


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st.integers())
def test_default_value(
    name: str,
    key: str,
    value: int,
) -> None:
    field_object = field(default=value)
    template_type = create(name, **{key: field_object})
    assert (result := init(template_type, **{key: value}))

    template = unwrap_success(result)
    assert template == Storage(**{key: value})


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st.integers(), default=st.integers())
def test_default_value_override(
    name: str,
    key: str,
    value: int,
    default: int,
) -> None:
    assume(value != default)

    field_object = field(default=value)
    template_type = create(name, **{key: field_object})
    assert (result := init(template_type, **{key: value}))

    template = unwrap_success(result)
    assert template == Storage(**{key: value})


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st.integers())
def test_any_value_matches_anything_in_required_field(
    name: str,
    key: str,
    value: int,
) -> None:
    field_object: FieldType[int] = field()
    template_type = create(name, **{key: field_object})
    assert (result := init(template_type, **{key: ANY}))

    template = unwrap_success(result)
    assert template == Storage(**{key: value})


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st.integers())
def test_any_value_matches_anything_in_optional_field(
    name: str,
    key: str,
    value: int,
) -> None:
    field_object: FieldType[int] = field(optional=True)
    template_type = create(name, **{key: field_object})
    assert (result := init(template_type, **{key: ANY}))

    template = unwrap_success(result)
    assert template == Storage(**{key: value})


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st.integers())
def test_wildcard_value_matches_anything_in_optional_field(
    name: str,
    key: str,
    value: int,
) -> None:
    field_object: FieldType[int] = field(optional=True)
    template_type = create(name, **{key: field_object})
    assert (result := init(template_type, **{key: WILDCARD}))

    template = unwrap_success(result)
    assert template == Storage()
    assert template == Storage(**{key: value})


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text())
def test_wildcard_value_error_in_required_field(
    name: str,
    key: str,
) -> None:
    field_object: FieldType[int] = field()
    template_type = create(name, **{key: field_object})
    assert not (result := init(template_type, **{key: WILDCARD}))

    error = unwrap_failure(result)
    assert isinstance(error, ProhibitedValueError)
    assert error.field == field_object
    assert error.value == WILDCARD


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text())
def test_absent_value_matches_anything_in_optional_field(
    name: str,
    key: str,
) -> None:
    field_object: FieldType[int] = field(optional=True)
    template_type = create(name, **{key: field_object})
    assert (result := init(template_type, **{key: ABSENT}))

    template = unwrap_success(result)
    assert template == Storage()


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st.integers())
def test_absent_value_mismatches_any_value_in_optional_field(
    name: str,
    key: str,
    value: int,
) -> None:
    field_object: FieldType[int] = field(optional=True)
    template_type = create(name, **{key: field_object})
    assert (result := init(template_type, **{key: ABSENT}))

    template = unwrap_success(result)
    assert template != Storage(**{key: value})


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text())
def test_absent_value_error_in_required_field(
    name: str,
    key: str,
) -> None:
    field_object: FieldType[int] = field()
    template_type = create(name, **{key: field_object})
    assert not (result := init(template_type, **{key: ABSENT}))

    error = unwrap_failure(result)
    assert isinstance(error, ProhibitedValueError)
    assert error.field == field_object
    assert error.value == ABSENT


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), other_key=st.text(), other_value=st.integers())
def test_unexpected_value_error(
    name: str,
    key: str,
    other_key: str,
    other_value: int,
) -> None:
    assume(key != other_key)

    field_object: FieldType[int] = field()
    template_type = create(name, **{key: field_object})
    assert not (result := init(template_type, **{other_key: other_value}))

    error = unwrap_failure(result)
    assert isinstance(error, UnexpectedValueError)
    assert error.key == other_key
    assert error.value == other_value


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text())
def test_missing_value_in_required_field_value_error(
    name: str,
    key: str,
) -> None:
    field_object: FieldType[int] = field()
    template_type = create(name, **{key: field_object})
    assert not (result := init(template_type))

    error = unwrap_failure(result)
    assert isinstance(error, MissingValueError)
    assert error.field == field_object


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text())
def test_optional_field_prevents_value_error_on_missing_value(
    name: str,
    key: str,
) -> None:
    field_object: FieldType[int] = field(optional=True)
    template_type = create(name, **{key: field_object})
    assert init(template_type)


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), default=st.integers())
def test_default_value_prevents_value_error_in_required_field_on_missing_value(
    name: str,
    key: str,
    default: int,
) -> None:
    field_object = field(default=default)
    template_type = create(name, **{key: field_object})
    assert init(template_type)


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), default=st.integers())
def test_default_value_prevents_value_error_in_optional_field_on_missing_value(
    name: str,
    key: str,
    default: int,
) -> None:
    field_object = field(default=default, optional=True)
    template_type = create(name, **{key: field_object})
    assert init(template_type)


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), default=st.integers())
def test_required_field_properties_access(
    name: str,
    key: str,
    default: int,
) -> None:
    field_object = field(default=default)
    template_type = create(name, **{key: field_object})
    template_fields = fields(template_type)

    assert template_fields[key].name == key
    assert template_fields[key].default == default
    assert template_fields[key].is_optional is False


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), default=st.integers())
def test_optional_field_properties_access(
    name: str,
    key: str,
    default: int,
) -> None:
    field_object = field(default=default, optional=True)
    template_type = create(name, **{key: field_object})
    template_fields = fields(template_type)

    assert template_fields[key].name == key
    assert template_fields[key].default == default
    assert template_fields[key].is_optional is True


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st.integers(), other_value=st.integers())
def test_modify(
    name: str,
    key: str,
    value: int,
    other_value: int,
) -> None:
    assume(value != other_value)

    field_object: FieldType[int] = field()
    template_type = create(name, **{key: field_object})
    assert (result := init(template_type, **{key: value}))

    template = unwrap_success(result)
    assert (modify_result := modify(template, **{key: other_value}))

    modified_template = unwrap_success(modify_result)
    assert template != modified_template
    assert template == Storage(**{key: value})
    assert modified_template == Storage(**{key: other_value})


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st.integers())
def test_value_of(
    name: str,
    key: str,
    value: int,
) -> None:
    field_object: FieldType[int] = field()
    template_type = create(name, **{key: field_object})
    assert (result := init(template_type, **{key: value}))

    template = unwrap_success(result)
    template_value = value_of(template)
    assert template_value == {key: value}


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st.integers())
def test_items(
    name: str,
    key: str,
    value: int,
) -> None:
    field_object: FieldType[int] = field()
    template_type = create(name, **{key: field_object})
    assert (result := init(template_type, **{key: value}))

    template = unwrap_success(result)
    template_value: Iterator[Tuple[str, Maybe[int], FieldType[int]]] = items(template)
    assert list(template_value) == [(key, value, field_object)]


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st.integers())
def test_error_forwarding(
    name: str,
    key: str,
    value: int,
) -> None:
    field_error = TestplatesError()
    field_object: FieldType[int] = field(failure(field_error))
    template_type = create(name, **{key: field_object})
    assert not (result := init(template_type, **{key: value}))

    error = unwrap_failure(result)
    assert isinstance(error, InvalidStructureError)
    assert error.errors == [field_error]
