from typing import TypeVar, Sequence

from resultful import unwrap_success, unwrap_failure
from hypothesis import given, strategies as st

from testplates import UNLIMITED
from testplates import sequence_validator
from testplates import InvalidTypeError

from tests.strategies import st_anything_except, st_anything_comparable

_T = TypeVar("_T")


def test_repr() -> None:
    assert (validator_result := sequence_validator(minimum_size=UNLIMITED, maximum_size=UNLIMITED))

    fmt = "testplates.SequenceValidator()"
    validator = unwrap_success(validator_result)
    assert repr(validator) == fmt


@given(data=st.lists(st_anything_comparable()))
def test_success(data: Sequence[_T]) -> None:
    assert (validator_result := sequence_validator(minimum_size=UNLIMITED, maximum_size=UNLIMITED))

    validator = unwrap_success(validator_result)
    assert (validation_result := validator(data))

    value = unwrap_success(validation_result)
    assert value is None


@given(data=st_anything_except(Sequence))
def test_failure_when_data_validation_fails(data: _T) -> None:
    assert (validator_result := sequence_validator(minimum_size=UNLIMITED, maximum_size=UNLIMITED))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == (Sequence,)
