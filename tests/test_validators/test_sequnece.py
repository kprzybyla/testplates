from typing import Any, TypeVar, List, Sequence

from resultful import failure, unwrap_success, unwrap_failure, Result
from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import UNLIMITED
from testplates import sequence_validator
from testplates import (
    TestplatesError,
    InvalidTypeError,
    InvalidMinimumSizeError,
    InvalidMaximumSizeError,
    UniquenessError,
    ItemValidationError,
)

from tests.utils import sample
from tests.strategies import st_hashable, st_anything_except, st_anything_comparable

_T = TypeVar("_T")


def test_repr() -> None:
    assert (validator_result := sequence_validator(minimum_size=UNLIMITED, maximum_size=UNLIMITED))

    fmt = "testplates.sequence_validator()"
    validator = unwrap_success(validator_result)
    assert repr(validator) == fmt


@given(data=st.lists(st_anything_comparable()))
def test_success(data: Sequence[_T]) -> None:
    assert (validator_result := sequence_validator(minimum_size=UNLIMITED, maximum_size=UNLIMITED))

    validator = unwrap_success(validator_result)
    assert (validation_result := validator(data))

    outcome = unwrap_success(validation_result)
    assert outcome is None


@given(data=st.lists(st_hashable(), min_size=1, unique=True))
def test_success_with_unique_value(data: Sequence[_T]) -> None:
    assert (
        validator_result := sequence_validator(
            minimum_size=UNLIMITED, maximum_size=UNLIMITED, unique_items=True
        )
    )

    validator = unwrap_success(validator_result)
    assert (validation_result := validator(data))

    outcome = unwrap_success(validation_result)
    assert outcome is None


@given(data=st_anything_except(Sequence))
def test_failure_when_data_validation_fails(data: _T) -> None:
    assert (validator_result := sequence_validator(minimum_size=UNLIMITED, maximum_size=UNLIMITED))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == (Sequence,)


@given(st_data=st.data(), data=st.lists(st_anything_comparable()))
def test_failure_when_value_does_not_fit_minimum_value(
    st_data: st.DataObject, data: Sequence[_T]
) -> None:
    minimum = st_data.draw(st.integers(min_value=len(data)))

    assume(len(data) < minimum)

    assert (validator_result := sequence_validator(minimum_size=minimum, maximum_size=UNLIMITED))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidMinimumSizeError)
    assert error.data == data
    assert error.minimum.value == minimum


@given(st_data=st.data(), data=st.lists(st_anything_comparable()))
def test_failure_when_value_does_not_fit_maximum_value(
    st_data: st.DataObject, data: Sequence[_T]
) -> None:
    maximum = st_data.draw(st.integers(max_value=len(data)))

    assume(len(data) > maximum)

    assert (validator_result := sequence_validator(minimum_size=UNLIMITED, maximum_size=maximum))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidMaximumSizeError)
    assert error.data == data
    assert error.maximum.value == maximum


@given(data=st.lists(st_hashable(), min_size=1, unique=True))
def test_failure_when_value_is_not_unique(data: List[_T]) -> None:
    data.append(sample(data))

    assert (
        validator_result := sequence_validator(
            minimum_size=UNLIMITED, maximum_size=UNLIMITED, unique_items=True
        )
    )

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, UniquenessError)
    assert error.data == data


@given(value=st_anything_comparable(), message=st.text())
def test_failure_when_data_item_validation_fails(value: Any, message: str) -> None:
    item_error = TestplatesError(message)

    def validator(this_value: Any, /) -> Result[None, TestplatesError]:
        assert this_value == value
        return failure(item_error)

    assert (
        validator_result := sequence_validator(
            validator, minimum_size=UNLIMITED, maximum_size=UNLIMITED
        )
    )

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator([value]))

    error = unwrap_failure(validation_result)
    assert isinstance(error, ItemValidationError)
    assert error.data == [value]
    assert error.item == value
    assert error.error == item_error
