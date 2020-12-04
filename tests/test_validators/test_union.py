from typing import (
    Any,
    Dict,
    NoReturn,
)

from resultful import (
    success,
    failure,
    unwrap_success,
    unwrap_failure,
    Result,
    AlwaysSuccess,
)

from hypothesis import (
    assume,
    given,
    strategies as st,
)

from testplates import (
    union_validator,
    passthrough_validator,
    Validator,
    TestplatesError,
    InvalidKeyError,
    InvalidTypeError,
    InvalidDataFormatError,
    ChoiceValidationError,
)

from tests.utils import (
    sample,
)

from tests.strategies import (
    st_anything_except,
    st_anything_comparable,
    Draw,
)


@st.composite
def st_choices(
    draw: Draw[Dict[str, AlwaysSuccess[Validator]]], min_size: int = 0
) -> Dict[str, AlwaysSuccess[Validator]]:
    def validator(data: Any) -> NoReturn:
        assert False, data

    return draw(st.dictionaries(st.text(), values=st.just(success(validator)), min_size=min_size))


# noinspection PyTypeChecker
@given(choices=st_choices())
def test_repr(choices: Dict[str, AlwaysSuccess[Validator]]) -> None:
    assert (validator_result := union_validator(choices))

    fmt = "testplates.union_validator({choices})"
    validator = unwrap_success(validator_result)
    union_choice = {key: unwrap_success(choice) for key, choice in choices.items()}
    assert repr(validator) == fmt.format(choices=union_choice)


# noinspection PyTypeChecker
@given(choices=st_choices(min_size=1), value=st_anything_comparable())
def test_success(choices: Dict[str, AlwaysSuccess[Validator]], value: Any) -> None:
    key = sample(choices)
    choices[key] = passthrough_validator()
    assert (validator_result := union_validator(choices))

    validator = unwrap_success(validator_result)
    assert (validation_result := validator((key, value)))

    outcome = unwrap_success(validation_result)
    assert outcome is None


# noinspection PyTypeChecker
@given(key=st.text())
def test_failure_when_choice_validator_fails(
    key: str,
) -> None:
    validator_error = TestplatesError()
    assert not (validator_result := union_validator({key: failure(validator_error)}))

    error = unwrap_failure(validator_result)
    assert error is validator_error


# noinspection PyTypeChecker
@given(choices=st_choices(min_size=1), key=st.text(), value=st_anything_comparable())
def test_failure_when_invalid_key_is_passed(
    choices: Dict[str, AlwaysSuccess[Validator]],
    key: str,
    value: Any,
) -> None:
    assume(key not in choices)
    assert (validator_result := union_validator(choices))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator((key, value)))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidKeyError)
    assert error.data == (key, value)


# noinspection PyTypeChecker
@given(choices=st_choices(min_size=1), value=st_anything_comparable())
def test_failure_when_invalid_tuple_format_is_passed(
    choices: Dict[str, AlwaysSuccess[Validator]],
    value: Any,
) -> None:
    key = sample(choices)
    choices[key] = passthrough_validator()
    assert (validator_result := union_validator(choices))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator((key, value, value)))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidDataFormatError)
    assert error.data == (key, value, value)


# noinspection PyTypeChecker
@given(choices=st_choices(min_size=1), data=st_anything_except(tuple))
def test_failure_when_data_type_validation_fails(
    choices: Dict[str, AlwaysSuccess[Validator]], data: Any
) -> None:
    assert (validator_result := union_validator(choices))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == (tuple,)


# noinspection PyTypeChecker
@given(choices=st_choices(min_size=1), value=st_anything_comparable(), message=st.text())
def test_failure_when_data_field_validation_fails(
    choices: Dict[str, AlwaysSuccess[Validator]],
    value: Any,
    message: str,
) -> None:
    choice_error = TestplatesError(message)

    def validator(this_value: Any, /) -> Result[None, TestplatesError]:
        assert this_value == value
        return failure(choice_error)

    key = sample(choices)
    choices[key] = success(validator)
    assert (validator_result := union_validator(choices))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator((key, value)))

    error = unwrap_failure(validation_result)
    assert isinstance(error, ChoiceValidationError)
    assert error.data == (key, value)
    assert error.error == choice_error
