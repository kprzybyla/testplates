import pytest

from hypothesis import given, assume
from hypothesis.strategies import integers

from testplates.value import MISSING

from testplates import (
    WILDCARD,
    ANY,
    ABSENT,
    MappingTemplate,
    Field,
    Required,
    Optional,
    DanglingDescriptorError,
    MissingValueError,
    UnexpectedValueError,
    ProhibitedValueError,
)


@given(value=integers())
def test_equality(value: int) -> None:
    class Template(MappingTemplate):

        valid: Required[int] = Field()

    assert Template(valid=value) == dict(valid=value)


@given(value=integers())
def test_inequality_due_to_different_key(value: int) -> None:
    class Template(MappingTemplate):

        valid: Required[int] = Field()

    assert Template(valid=value) != dict(invalid=value)


@given(value=integers(), other=integers())
def test_inequality_due_to_different_value(value: int, other: int) -> None:
    assume(value != other)

    class Template(MappingTemplate):

        valid: Required[int] = Field()

    assert Template(valid=value) != dict(valid=other)


@given(value=integers())
def test_default_value(value: int) -> None:
    class Template(MappingTemplate):

        valid: Required[int] = Field(default=value)

    assert Template() == dict(valid=value)


@given(value=integers(), default=integers())
def test_default_value_override(value: int, default: int) -> None:
    assume(value != default)

    class Template(MappingTemplate):

        valid: Required[int] = Field(default=default)

    assert Template(valid=value) == dict(valid=value)


@given(value=integers())
def test_any_value_matches_on_optional_field(value: int) -> None:
    class Template(MappingTemplate):

        valid: Optional[int] = Field(optional=True)

    assert Template(valid=ANY) == dict(valid=value)


@given(value=integers())
def test_wildcard_value_matches_on_optional_field(value: int) -> None:
    class Template(MappingTemplate):

        valid: Optional[int] = Field(optional=True)

    assert Template(valid=WILDCARD) == dict()
    assert Template(valid=WILDCARD) == dict(valid=value)


def test_wildcard_value_raises_value_error_on_required_field() -> None:
    class Template(MappingTemplate):

        valid: Required[int] = Field()

    with pytest.raises(ValueError):
        Template(valid=WILDCARD)

    with pytest.raises(ProhibitedValueError):
        Template(valid=WILDCARD)


def test_absent_value_matches_on_optional_field() -> None:
    class Template(MappingTemplate):

        valid: Optional[int] = Field(optional=True)

    assert Template(valid=ABSENT) == dict()


@given(value=integers())
def test_absent_value_mismatches_on_optional_field(value: int) -> None:
    class Template(MappingTemplate):

        valid: Optional[int] = Field(optional=True)

    assert Template(valid=ABSENT) != dict(valid=value)


def test_absent_value_raises_value_error_on_required_field() -> None:
    class Template(MappingTemplate):

        valid: Required[int] = Field()

    with pytest.raises(ValueError):
        Template(valid=ABSENT)

    with pytest.raises(ProhibitedValueError):
        Template(valid=ABSENT)


def test_missing_required_field_value_raises_missing_value_error() -> None:
    class Template(MappingTemplate):

        valid: Required[int] = Field()

    with pytest.raises(ValueError):
        Template()

    with pytest.raises(MissingValueError):
        Template()


def test_missing_optional_field_value_raises_missing_value_error() -> None:
    class Template(MappingTemplate):

        valid: Optional[int] = Field(optional=True)

    with pytest.raises(ValueError):
        Template()

    with pytest.raises(MissingValueError):
        Template()


@given(value=integers())
def test_required_field_with_default_value_does_not_raise_missing_value_error(value: int) -> None:
    class Template(MappingTemplate):

        valid: Required[int] = Field(default=value)

    Template()


@given(value=integers())
def test_optional_field_with_default_value_does_not_raise_missing_value_error(value: int) -> None:
    class Template(MappingTemplate):

        valid: Optional[int] = Field(default=value, optional=True)

    Template()


@given(value=integers())
def test_extra_value_raises_value_error(value: int) -> None:
    class Template(MappingTemplate):
        pass

    with pytest.raises(ValueError):
        Template(OTHER_FIELD_NAME=value)

    with pytest.raises(UnexpectedValueError):
        Template(OTHER_FIELD_NAME=value)


@given(value=integers())
def test_nested_templates(value: int) -> None:
    class Inner(MappingTemplate):

        valid: Required[int] = Field()

    class Outer(MappingTemplate):

        inner: Required[Inner] = Field()

    assert Outer(inner=Inner(valid=value)) == dict(inner=dict(valid=value))


@given(value=integers(), default=integers())
def test_access_and_properties(value: int, default: int) -> None:
    class Template(MappingTemplate):

        valid: Optional[int] = Field(default=default, optional=True)

    mapping = Template(valid=value)

    assert mapping["valid"] == value
    assert Template.valid.name == "valid"
    assert Template.valid.default == default
    assert Template.valid.is_optional


@given(default=integers())
def test_access_1(default: int) -> None:
    class Template(MappingTemplate):

        valid: Required[int] = Field(default=default)

    mapping = Template()

    assert mapping["valid"] == default
    assert len(mapping) == 1
    assert list(iter(mapping)) == ["valid"]


def test_dangling_descriptor_error():
    valid = Field()

    with pytest.raises(DanglingDescriptorError):
        valid.name
