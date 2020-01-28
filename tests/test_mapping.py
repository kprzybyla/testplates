import pytest

from hypothesis import given, assume
from hypothesis.strategies import integers

from testplates import (
    WILDCARD,
    ABSENT,
    Mapping,
    Field,
    Required,
    Optional,
    MissingValueError,
    UnexpectedValueError,
    ProhibitedValueError,
)

FIELD_NAME = "count"
OTHER_FIELD_NAME = "name"


@given(value=integers())
def test_equality(value):
    class TestMapping(Mapping):

        count: Required[int] = Field()

    assert TestMapping(count=value) == {FIELD_NAME: value}


@given(value=integers())
def test_inequality_due_to_different_key(value):
    class TestMapping(Mapping):

        count: Required[int] = Field()

    assert TestMapping(count=value) != {OTHER_FIELD_NAME: value}


@given(value=integers(), other=integers())
def test_inequality_due_to_different_value(value, other):
    assume(value != other)

    class TestMapping(Mapping):

        count: Required[int] = Field()

    assert TestMapping(count=value) != {FIELD_NAME: other}


@given(value=integers())
def test_default_value(value):
    class TestMapping(Mapping):

        count: Required[int] = Field(default=value)

    assert TestMapping() == {FIELD_NAME: value}


@given(value=integers(), default=integers())
def test_default_value_override(value, default):
    assume(value != default)

    class TestMapping(Mapping):

        count: Required[int] = Field(default=default)

    assert TestMapping(count=value) == {FIELD_NAME: value}


@given(value=integers())
def test_wildcard_value_matches_on_optional_field(value):
    class TestMapping(Mapping):

        count: Optional[int] = Field(optional=True)

    assert TestMapping(count=WILDCARD) == {}
    assert TestMapping(count=WILDCARD) == {FIELD_NAME: value}


def test_wildcard_value_raises_value_error_on_required_field():
    class TestMapping(Mapping):

        count: Required[int] = Field()

    with pytest.raises(ValueError):
        TestMapping(count=WILDCARD)

    with pytest.raises(ProhibitedValueError):
        TestMapping(count=WILDCARD)


def test_absent_value_matches_on_optional_field():
    class TestMapping(Mapping):

        count: Optional[int] = Field(optional=True)

    assert TestMapping(count=ABSENT) == {}


@given(value=integers())
def test_absent_value_mismatches_on_optional_field(value):
    class TestMapping(Mapping):

        count: Optional[int] = Field(optional=True)

    assert TestMapping(count=ABSENT) != {FIELD_NAME: value}


def test_absent_value_raises_value_error_on_required_field():
    class TestMapping(Mapping):

        count: Required[int] = Field()

    with pytest.raises(ValueError):
        TestMapping(count=ABSENT)

    with pytest.raises(ProhibitedValueError):
        TestMapping(count=ABSENT)


def test_missing_required_field_value_raises_missing_value_error():
    class TestMapping(Mapping):

        count: Required[int] = Field()

    with pytest.raises(ValueError):
        TestMapping()

    with pytest.raises(MissingValueError):
        TestMapping()


def test_missing_optional_field_value_raises_missing_value_error():
    class TestMapping(Mapping):

        count: Optional[int] = Field(optional=True)

    with pytest.raises(ValueError):
        TestMapping()

    with pytest.raises(MissingValueError):
        TestMapping()


@given(value=integers())
def test_field_with_default_value_does_not_raise_missing_value_error(value):
    class TestMapping(Mapping):

        count: Required[int] = Field(default=value)
        counter: Optional[int] = Field(default=value, optional=True)

    TestMapping()


@given(value=integers())
def test_extra_value_raises_value_error(value):
    class TestMapping(Mapping):
        pass

    with pytest.raises(ValueError):
        TestMapping(OTHER_FIELD_NAME=value)

    with pytest.raises(UnexpectedValueError):
        TestMapping(OTHER_FIELD_NAME=value)


@given(value=integers(), default=integers())
def test_access_and_properties(value, default):
    class TestMapping(Mapping):

        count: Optional[int] = Field(default=default, optional=True)

    mapping = TestMapping(count=value)

    assert mapping[FIELD_NAME] == value
    assert TestMapping[FIELD_NAME].default == default
    assert TestMapping[FIELD_NAME].is_optional
