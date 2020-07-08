from typing import Any, Dict, NoReturn

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates.result import Success, Failure
from testplates.validators import union_validator, passthrough_validator, Validator
from testplates.validators.exceptions import (
    ValidationError,
    InvalidKeyError,
    InvalidTypeError,
    ChoiceValidationError,
)

from tests.conftest import sample, st_anything_except, st_anything_comparable, Draw


@st.composite
def st_choices(draw: Draw[Dict[str, Validator]], min_size: int = 0) -> Dict[str, Validator]:
    def bad_validator(data: Any) -> NoReturn:
        raise Exception(f"This validator should never be called (data={data!r})")

    return draw(st.dictionaries(st.text(), values=st.just(bad_validator), min_size=min_size))


@given(choices=st_choices())
def test_repr(choices: Dict[str, Validator]) -> None:
    fmt = "testplates.union_validator({choices})"

    validator_result = union_validator(choices)
    validator = Success.get_value(validator_result)

    assert repr(validator) == fmt.format(choices=choices)


@given(choices=st_choices(min_size=1), value=st_anything_comparable())
def test_success(choices: Dict[str, Validator], value: Any) -> None:
    key = sample(choices)

    choices[key] = passthrough_validator
    data = (key, value)

    validator_result = union_validator(choices)
    validator = Success.from_result(validator_result).value

    validation_result = validator(data)
    value = Success.get_value(validation_result)

    assert value is None


@given(choices=st_choices(min_size=1), key=st.text(), value=st_anything_comparable())
def test_failure_when_invalid_key_is_passed(
    choices: Dict[str, Validator], key: str, value: Any
) -> None:
    assume(key not in choices)

    data = (key, value)

    validator_result = union_validator(choices)
    validator = Success.from_result(validator_result).value

    validation_result = validator(data)
    error = Failure.get_error(validation_result)

    assert isinstance(error, InvalidKeyError)
    assert error.data is data


@given(choices=st_choices(min_size=1), data=st_anything_except(tuple))
def test_failure_when_data_type_validation_fails(choices: Dict[str, Validator], data: Any) -> None:
    validator_result = union_validator(choices)
    validator = Success.get_value(validator_result)

    validation_result = validator(data)
    error = Failure.get_error(validation_result)

    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == (tuple,)


# noinspection PyTypeChecker
@given(choices=st_choices(min_size=1), value=st_anything_comparable(), message=st.text())
def test_failure_when_data_field_validation_fails(
    choices: Dict[str, Validator], value: Any, message: str
) -> None:
    failure = Failure(ValidationError(message))

    def validator(this_value: Any) -> Failure[ValidationError]:
        assert this_value is value
        return failure

    key = sample(choices)

    choices[key] = validator
    data = (key, value)

    validator_result = union_validator(choices)
    validator = Success.get_value(validator_result)

    validation_result = validator(data)
    error = Failure.get_error(validation_result)

    assert isinstance(error, ChoiceValidationError)
    assert error.data is data
    assert error.error is failure
