from string import printable

from typing import (
    List,
    NoReturn,
)

from resultful import (
    success,
    failure,
    unwrap_failure,
    Result,
)

from hypothesis import (
    given,
    strategies as st,
)

from testplates import (
    create,
    init,
    field,
    FieldType,
    ANY,
    WILDCARD,
    ABSENT,
    TestplatesError,
)

from tests.strategies import (
    st_anything_comparable,
    Draw,
)


@st.composite
def st_name(draw: Draw[str]) -> str:
    return draw(st.text(printable))


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text())
def test_repr_for_required_field_without_default_value(
    name: str,
    key: str,
) -> None:
    field_object: FieldType[int] = field()
    create(name, **{key: field_object})

    repr_format = f"testplates.Field({key!r}, optional=False)"
    assert repr(field_object) == repr_format


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st_anything_comparable())
def test_repr_for_required_field_with_default_value(
    name: str,
    key: str,
    value: int,
) -> None:
    field_object = field(default=value)
    create(name, **{key: field_object})

    repr_format = f"testplates.Field({key!r}, default={value!r}, optional=False)"
    assert repr(field_object) == repr_format


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text())
def test_repr_for_optional_field_without_default_value(
    name: str,
    key: str,
) -> None:
    field_object: FieldType[int] = field(optional=True)
    create(name, **{key: field_object})

    repr_format = f"testplates.Field({key!r}, optional=True)"
    assert repr(field_object) == repr_format


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st_anything_comparable())
def test_repr_for_optional_field_with_default_value(
    name: str,
    key: str,
    value: int,
) -> None:
    field_object = field(default=value, optional=True)
    create(name, **{key: field_object})

    repr_format = f"testplates.Field({key!r}, default={value!r}, optional=True)"
    assert repr(field_object) == repr_format


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text())
def test_validator_is_not_called_on_special_value_for_required_field(
    name: str,
    key: str,
) -> None:
    def validator(*args: int, **kwargs: int) -> NoReturn:
        assert False, (args, kwargs)

    field_object: FieldType[int] = field(success(validator))
    template_type = create(name, **{key: field_object})
    assert init(template_type, **{key: ANY})


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text())
def test_validator_is_not_called_on_special_value_for_optional_field(
    name: str,
    key: str,
) -> None:
    def validator(*args: int, **kwargs: int) -> NoReturn:
        assert False, (args, kwargs)

    field_object: FieldType[int] = field(success(validator), optional=True)
    template_type = create(name, **{key: field_object})
    assert init(template_type, **{key: ANY})
    assert init(template_type, **{key: WILDCARD})
    assert init(template_type, **{key: ABSENT})


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st_anything_comparable(), message=st.text())
def test_validator_failure(
    name: str,
    key: str,
    value: int,
    message: str,
) -> None:
    validator_error = TestplatesError(message)

    def validator(this_value: int, /) -> Result[None, TestplatesError]:
        assert this_value is value
        return failure(validator_error)

    field_object: FieldType[int] = field(success(validator))
    template_type = create(name, **{key: field_object})
    assert not (result := init(template_type, **{key: value}))

    error = unwrap_failure(result)
    assert isinstance(error, TestplatesError)
    assert error.message == message


# noinspection PyTypeChecker
def test_default_for_mutable_objects() -> None:
    field_object: FieldType[List[int]] = field(default=list())
    assert field_object.default is field_object.default


# noinspection PyTypeChecker
def test_default_factory_for_mutable_objects() -> None:
    field_object = field(default_factory=list)
    assert field_object.default is not field_object.default
