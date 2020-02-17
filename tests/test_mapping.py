from hypothesis import given
from hypothesis.strategies import integers

from testplates import Mapping, field, Required, Optional


@given(value=integers())
def test_nested_templates(value: int) -> None:
    class Inner(Mapping):

        valid: Required[int] = field()

    class Outer(Mapping):

        inner: Required[Inner] = field()

    assert Outer(inner=Inner(valid=value)) == dict(inner=dict(valid=value))


@given(value=integers(), default=integers())
def test_access_and_properties(value: int, default: int) -> None:
    class Template(Mapping):

        valid: Optional[int] = field(default=default, optional=True)

    mapping = Template(valid=value)

    assert mapping["valid"] == value
    assert Template.valid.name == "valid"
    assert Template.valid.default == default
    assert Template.valid.is_optional


@given(default=integers())
def test_access_1(default: int) -> None:
    class Template(Mapping):

        valid: Required[int] = field(default=default)

    mapping = Template()

    assert mapping["valid"] == default
    assert len(mapping) == 1
    assert list(iter(mapping)) == ["valid"]
