from string import printable

from typing import (
    List,
    NoReturn,
)

import pytest

from resultful import (
    failure,
    unwrap_failure,
    Result,
)

from hypothesis import (
    given,
    strategies as st,
)

from testplates import (
    initialize,
    field,
    ANY,
    WILDCARD,
    ABSENT,
    TestplatesError,
    DanglingDescriptorError,
)

from tests.strategies import (
    st_anything_comparable,
    Draw,
)

from .assets import CreateFunctionType
from .conftest import create_function_parameters


@st.composite
def st_name(draw: Draw[str]) -> str:
    return draw(st.text(printable))


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text())
@create_function_parameters
def test_repr_for_required_field_without_default_value(
    name: str,
    key: str,
    create_function: CreateFunctionType,
) -> None:
    field_object = field(int)
    create_function(name, **{key: field_object})

    repr_format = f"testplates.Field({key!r}, optional=False)"
    assert repr(field_object) == repr_format


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st_anything_comparable())
@create_function_parameters
def test_repr_for_required_field_with_default_value(
    name: str,
    key: str,
    value: int,
    create_function: CreateFunctionType,
) -> None:
    field_object = field(int, default=value)
    create_function(name, **{key: field_object})

    repr_format = f"testplates.Field({key!r}, default={value!r}, optional=False)"
    assert repr(field_object) == repr_format


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text())
@create_function_parameters
def test_repr_for_optional_field_without_default_value(
    name: str,
    key: str,
    create_function: CreateFunctionType,
) -> None:
    field_object = field(int, optional=True)
    create_function(name, **{key: field_object})

    repr_format = f"testplates.Field({key!r}, optional=True)"
    assert repr(field_object) == repr_format


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st_anything_comparable())
@create_function_parameters
def test_repr_for_optional_field_with_default_value(
    name: str,
    key: str,
    value: int,
    create_function: CreateFunctionType,
) -> None:
    field_object = field(int, default=value, optional=True)
    create_function(name, **{key: field_object})

    repr_format = f"testplates.Field({key!r}, default={value!r}, optional=True)"
    assert repr(field_object) == repr_format


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text())
@create_function_parameters
def test_validator_is_not_called_on_special_value_for_required_field(
    name: str,
    key: str,
    create_function: CreateFunctionType,
) -> None:
    def validator(*args: int, **kwargs: int) -> NoReturn:
        assert False, (args, kwargs)

    field_object = field(int, validator)
    template_type = create_function(name, **{key: field_object})
    assert initialize(template_type(), **{key: ANY})


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text())
@create_function_parameters
def test_validator_is_not_called_on_special_value_for_optional_field(
    name: str,
    key: str,
    create_function: CreateFunctionType,
) -> None:
    def validator(*args: int, **kwargs: int) -> NoReturn:
        assert False, (args, kwargs)

    field_object = field(int, validator, optional=True)
    template_type = create_function(name, **{key: field_object})
    assert initialize(template_type(), **{key: ANY})
    assert initialize(template_type(), **{key: WILDCARD})
    assert initialize(template_type(), **{key: ABSENT})


# noinspection PyTypeChecker
@given(name=st_name(), key=st.text(), value=st_anything_comparable(), message=st.text())
@create_function_parameters
def test_validator_failure(
    name: str,
    key: str,
    value: int,
    message: str,
    create_function: CreateFunctionType,
) -> None:
    validator_error = TestplatesError(message)

    def validator(this_value: int, /) -> Result[None, TestplatesError]:
        assert this_value is value
        return failure(validator_error)

    field_object = field(int, validator)
    template_type = create_function(name, **{key: field_object})
    assert not (result := initialize(template_type(), **{key: value}))

    error = unwrap_failure(result)
    assert isinstance(error, TestplatesError)
    assert error.message == message


def test_name_raises_dangling_descriptor_error_when_specified_outside_the_class() -> None:
    field_object = field(int)

    with pytest.raises(DanglingDescriptorError) as exception:
        print(field_object.name)

    assert exception.value.descriptor == field_object


# noinspection PyTypeChecker
def test_default_for_mutable_objects() -> None:
    field_object = field(List[int], default=list())
    assert field_object.default is field_object.default


# noinspection PyTypeChecker
def test_default_factory_for_mutable_objects() -> None:
    field_object = field(List[int], default_factory=list)
    assert field_object.default is not field_object.default
