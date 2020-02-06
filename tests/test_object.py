from hypothesis import given
from hypothesis.strategies import integers

from testplates import ObjectTemplate, Field, Optional


@given(value=integers(), default=integers())
def test_access_and_properties(value: int, default: int) -> None:
    class Template(ObjectTemplate):

        valid: Optional[int] = Field(default=default, optional=True)

    mapping = Template(valid=value)

    assert mapping.valid == value
    assert Template.valid.name == "valid"
    assert Template.valid.default == default
    assert Template.valid.is_optional
