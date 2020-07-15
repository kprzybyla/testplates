from typing import TypeVar, Sequence

from hypothesis import given, strategies as st

from testplates import Success, Failure
from testplates.boundaries import UNLIMITED
from testplates.validators import sequence_validator
from testplates.validators.exceptions import InvalidTypeError

from tests.conftest import st_anything_except, st_anything_comparable

_T = TypeVar("_T")


def test_repr() -> None:
    fmt = "testplates.sequence_validator()"

    validator_result = sequence_validator(minimum_size=UNLIMITED, maximum_size=UNLIMITED)
    validator = Success.get_value(validator_result)

    assert repr(validator) == fmt


@given(data=st.lists(st_anything_comparable()))
def test_success(data: Sequence) -> None:
    validator_result = sequence_validator(minimum_size=UNLIMITED, maximum_size=UNLIMITED)
    validator = Success.get_value(validator_result)

    validation_result = validator(data)
    value = Success.get_value(validation_result)

    assert value is None


@given(data=st_anything_except(Sequence))
def test_failure_when_data_validation_fails(data: _T) -> None:
    validator_result = sequence_validator(minimum_size=UNLIMITED, maximum_size=UNLIMITED)
    validator = Success.get_value(validator_result)

    validation_result = validator(data)
    error = Failure.get_error(validation_result)

    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == (Sequence,)
