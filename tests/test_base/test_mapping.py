from typing import Final

from resultful import unwrap_success
from hypothesis import given
from hypothesis import strategies as st

from testplates import initialize, field, Mapping, Required, Optional

KEY: Final[str] = "key"


@given(value=st.integers())
def test_value_access_in_required_field(value: int) -> None:
    class Template(Mapping[int]):

        key: Required[int] = field(int)

    assert (result := initialize(Template(), key=value))

    template = unwrap_success(result)
    assert template[KEY] == value


@given(value=st.integers(), default=st.integers())
def test_value_access_in_required_field_with_default_value(value: int, default: int) -> None:
    class Template(Mapping[int]):

        key: Required[int] = field(int, default=default)

    assert (result_value := initialize(Template(), key=value))
    assert (result_default := initialize(Template()))

    template_value = unwrap_success(result_value)
    template_default = unwrap_success(result_default)
    assert template_value[KEY] == value
    assert template_default[KEY] == default


@given(value=st.integers())
def test_value_access_in_optional_field(value: int) -> None:
    class Template(Mapping[int]):

        key: Optional[int] = field(int, optional=True)

    assert (result := initialize(Template(), key=value))

    template = unwrap_success(result)
    assert template[KEY] == value


@given(value=st.integers(), default=st.integers())
def test_value_access_in_optional_field_with_default_value(value: int, default: int) -> None:
    class Template(Mapping[int]):

        key: Optional[int] = field(int, default=default, optional=True)

    assert (result_value := initialize(Template(), key=value))
    assert (result_default := initialize(Template()))

    template_value = unwrap_success(result_value)
    template_default = unwrap_success(result_default)
    assert template_value[KEY] == value
    assert template_default[KEY] == default


@given(value=st.integers())
def test_len(value: int) -> None:
    class Template(Mapping[int]):

        key: Required[int] = field(int)

    assert (result := initialize(Template(), key=value))

    template = unwrap_success(result)
    assert len(template) == 1


@given(value=st.integers())
def test_iter(value: int) -> None:
    class Template(Mapping[int]):

        key: Required[int] = field(int)

    assert (result := initialize(Template(), key=value))

    template = unwrap_success(result)
    assert list(iter(template)) == [KEY]
