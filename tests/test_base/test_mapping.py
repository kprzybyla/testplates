from typing import Final

from resultful import unwrap_success

from hypothesis import (
    given,
    strategies as st,
)

from testplates import (
    struct,
    init,
    field,
    passthrough_validator,
    MISSING,
)

KEY: Final[str] = "key"


# noinspection PyTypeChecker
@given(value=st.integers())
def test_value_access_in_required_field(value: int) -> None:
    @struct
    class Template:

        key = field()

    validator = unwrap_success(passthrough_validator())
    assert Template.key.name == KEY
    assert Template.key.default == MISSING
    assert Template.key.validator is validator
    assert Template.key.is_optional is False

    assert (result := init(Template, key=value))

    template = unwrap_success(result)
    assert template.key == value
    assert template[KEY] == value


# noinspection PyTypeChecker
@given(value=st.integers(), default=st.integers())
def test_value_access_in_required_field_with_default_value(value: int, default: int) -> None:
    @struct
    class Template:

        key = field(default=default)

    validator = unwrap_success(passthrough_validator())
    assert Template.key.name == KEY
    assert Template.key.default == default
    assert Template.key.validator is validator
    assert Template.key.is_optional is False

    assert (result_value := init(Template, key=value))
    assert (result_default := init(Template))

    template_value = unwrap_success(result_value)
    template_default = unwrap_success(result_default)
    assert template_value.key == value
    assert template_value[KEY] == value
    assert template_default.key == default
    assert template_default[KEY] == default


# noinspection PyTypeChecker
@given(value=st.integers())
def test_value_access_in_optional_field(value: int) -> None:
    @struct
    class Template:

        key = field(optional=True)

    validator = unwrap_success(passthrough_validator())
    assert Template.key.name == KEY
    assert Template.key.default == MISSING
    assert Template.key.validator is validator
    assert Template.key.is_optional is True

    assert (result := init(Template, key=value))

    template = unwrap_success(result)
    assert template.key == value
    assert template[KEY] == value


# noinspection PyTypeChecker
@given(value=st.integers(), default=st.integers())
def test_value_access_in_optional_field_with_default_value(value: int, default: int) -> None:
    @struct
    class Template:

        key = field(default=default, optional=True)

    validator = unwrap_success(passthrough_validator())
    assert Template.key.name == KEY
    assert Template.key.default == default
    assert Template.key.validator is validator
    assert Template.key.is_optional is True

    assert (result_value := init(Template, key=value))
    assert (result_default := init(Template))

    template_value = unwrap_success(result_value)
    template_default = unwrap_success(result_default)
    assert template_value.key == value
    assert template_value[KEY] == value
    assert template_default.key == default
    assert template_default[KEY] == default


# noinspection PyTypeChecker
@given(value=st.integers())
def test_len(value: int) -> None:
    @struct
    class Template:

        key = field()

    assert (result := init(Template, key=value))

    template = unwrap_success(result)
    assert len(template) == 1


# noinspection PyTypeChecker
@given(value=st.integers())
def test_iter(value: int) -> None:
    @struct
    class Template:

        key = field()

    assert (result := init(Template, key=value))

    template = unwrap_success(result)
    assert list(iter(template)) == [KEY]
