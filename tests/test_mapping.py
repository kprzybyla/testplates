import pytest

from testplates import Mapping, Field, ABSENT


def test_mapping_matching():
    class MyMapping(Mapping):

        value = Field()

    assert MyMapping(value=5) == {"value": 5}
    assert MyMapping(value=5) != {"value": 10}


def test_mapping_default_value():
    class MyMapping(Mapping):

        value = Field(default=5)

    assert MyMapping() == {"value": 5}
    assert MyMapping() != {"value": 10}


def test_mapping_default_value_override():
    class MyMapping(Mapping):

        value = Field(default=10)

    assert MyMapping(value=5) == {"value": 5}
    assert MyMapping(value=5) != {"value": 10}


def test_mapping_optional():
    class MyMapping(Mapping):

        value = Field(optional=True)

    assert MyMapping(value=ABSENT) == {}


def test_mapping_optional_not_set_to_omit():
    class MyMapping(Mapping):

        value = Field(optional=True)

    with pytest.raises(ValueError):
        MyMapping()


def test_mapping_access():
    class MyMapping(Mapping):

        value = Field(default=5, optional=True)

    mapping = MyMapping(value=10)

    assert mapping["value"] == 10
    assert MyMapping["value"].default == 5
    assert MyMapping["value"].is_optional
