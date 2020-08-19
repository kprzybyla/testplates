import pytest

from typing import List, NoReturn

from resultful import failure, unwrap_failure, Result
from hypothesis import given
from hypothesis import strategies as st

from testplates import ANY, WILDCARD, ABSENT
from testplates import field, Required, Optional, Object
from testplates import TestplatesError, InvalidSignatureError, DanglingDescriptorError

from tests.strategies import st_anything_comparable


def test_repr_for_required_field_without_default_value() -> None:
    fmt = "testplates.Field('key', optional=False)"

    class Template(Object[int]):

        key: Required[int] = field(int)

    assert repr(Template.key) == fmt.format()


@given(value=st_anything_comparable())
def test_repr_for_required_field_with_default_value(value: int) -> None:
    fmt = "testplates.Field('key', default={value}, optional=False)"

    class Template(Object[int]):

        key: Required[int] = field(int, default=value)

    assert repr(Template.key) == fmt.format(value=repr(value))


def test_repr_for_optional_field_without_default_value() -> None:
    fmt = "testplates.Field('key', optional=True)"

    class Template(Object[int]):

        key: Optional[int] = field(int, optional=True)

    assert repr(Template.key) == fmt.format()


@given(value=st_anything_comparable())
def test_repr_for_optional_field_with_default_value(value: int) -> None:
    fmt = "testplates.Field('key', default={value}, optional=True)"

    class Template(Object[int]):

        key: Optional[int] = field(int, default=value, optional=True)

    assert repr(Template.key) == fmt.format(value=repr(value))


def test_validator_is_not_called_on_special_value_for_required_field() -> None:
    def validator(*args: int, **kwargs: int) -> NoReturn:
        raise NotImplementedError(args, kwargs)

    class Template(Object[int]):

        key: Required[int] = field(int, validator)

    assert Template()._init_(key=ANY)


def test_validator_is_not_called_on_special_value_for_optional_field() -> None:
    def validator(*args: int, **kwargs: int) -> NoReturn:
        raise NotImplementedError(args, kwargs)

    class Template(Object[int]):

        key: Optional[int] = field(int, validator, optional=True)

    assert Template()._init_(key=ANY)
    assert Template()._init_(key=WILDCARD)
    assert Template()._init_(key=ABSENT)


@given(value=st_anything_comparable(), message=st.text())
def test_validator_failure(value: int, message: str) -> None:
    validator_error = TestplatesError(message)

    def validator(this_value: int, /) -> Result[None, TestplatesError]:
        assert this_value is value
        return failure(validator_error)

    class Template(Object[int]):

        key: Required[int] = field(int, validator)

    assert not (result := Template()._init_(key=value))

    error = unwrap_failure(result)
    assert isinstance(error, TestplatesError)
    assert error.message == message


def test_name_raises_dangling_descriptor_error_when_specified_outside_the_class() -> None:
    field_object: Required[int] = field(int)

    with pytest.raises(DanglingDescriptorError) as exception:
        print(field_object.name)

    assert exception.value.descriptor == field_object


# noinspection PyTypeChecker
def test_default_for_mutable_objects() -> None:
    field_object: Required[List[int]] = field(List[int], default=list())

    assert field_object.default is field_object.default


# noinspection PyTypeChecker
def test_default_factory_for_mutable_objects() -> None:
    field_object: Required[List[int]] = field(List[int], default_factory=list)

    assert field_object.default is not field_object.default


# noinspection PyArgumentList
def test_default_and_default_factory_type_error() -> None:
    with pytest.raises(InvalidSignatureError):
        field(int, default=list(), default_factory=list)  # type: ignore
