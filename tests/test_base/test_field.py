import pytest

from typing import Any, List, NoReturn
from hypothesis import given, strategies as st

from testplates import (
    failure,
    Result,
)

from testplates import (
    field,
    Required,
    Optional,
    Object,
    ANY,
    WILDCARD,
    ABSENT,
)

from testplates import (
    ValidationError,
    DanglingDescriptorError,
)

from tests.conftest import st_anything_comparable


def test_repr_for_required_field_without_default_value() -> None:
    fmt = "testplates.Field('key', optional=False)"

    class Template(Object):

        key: Required[Any] = field()

    assert repr(Template.key) == fmt.format()


@given(value=st_anything_comparable())
def test_repr_for_required_field_with_default_value(value: Any) -> None:
    fmt = "testplates.Field('key', default={value}, optional=False)"

    class Template(Object):

        key: Required[Any] = field(default=value)

    assert repr(Template.key) == fmt.format(value=repr(value))


def test_repr_for_optional_field_without_default_value() -> None:
    fmt = "testplates.Field('key', optional=True)"

    class Template(Object):

        key: Optional[Any] = field(optional=True)

    assert repr(Template.key) == fmt.format()


@given(value=st_anything_comparable())
def test_repr_for_optional_field_with_default_value(value: Any) -> None:
    fmt = "testplates.Field('key', default={value}, optional=True)"

    class Template(Object):

        key: Optional[Any] = field(default=value, optional=True)

    assert repr(Template.key) == fmt.format(value=repr(value))


def test_validator_is_not_called_on_special_value_for_required_field() -> None:
    def validator(*args, **kwargs) -> NoReturn:
        raise NotImplementedError(args, kwargs)

    class Template(Object):

        key: Required[Any] = field(validator)

    Template(key=ANY)


def test_validator_is_not_called_on_special_value_for_optional_field() -> None:
    def validator(*args, **kwargs) -> NoReturn:
        raise NotImplementedError(args, kwargs)

    class Template(Object):

        key: Optional[Any] = field(validator, optional=True)

    Template(key=ANY)
    Template(key=WILDCARD)
    Template(key=ABSENT)


# noinspection PyTypeChecker
@given(value=st_anything_comparable(), message=st.text())
def test_validator_failure(value: Any, message: str) -> None:
    failure_object = failure(ValidationError(message))

    # noinspection PyTypeChecker
    def validator(this_value: Any) -> Result[None, ValidationError]:
        assert this_value is value
        return failure_object

    class Template(Object):

        key: Required[Any] = field(validator)

    with pytest.raises(ValidationError) as exception:
        Template(key=value)

    assert exception.value.message == message


def test_name_raises_dangling_descriptor_error_when_specified_outside_the_class() -> None:
    key: Required[Any] = field()

    with pytest.raises(DanglingDescriptorError):
        print(key.name)


def test_default_for_mutable_objects():
    key: Required[List[Any]] = field(default=list())

    assert key.default is key.default


def test_default_factory_for_mutable_objects():
    key: Required[List[Any]] = field(default_factory=list)

    assert key.default is not key.default


# noinspection PyArgumentList
def test_default_and_default_factory_type_error():
    with pytest.raises(TypeError):
        field(default=list(), default_factory=list)  # type: ignore
