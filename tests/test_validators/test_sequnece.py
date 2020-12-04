import sys

from typing import (
    Any,
    List,
    Sequence,
    Hashable,
    Literal,
    Final,
)

from resultful import (
    success,
    failure,
    unwrap_success,
    unwrap_failure,
    Result,
)

from hypothesis import (
    assume,
    given,
    strategies as st,
)

from testplates import (
    sequence_validator,
    TestplatesError,
    InvalidTypeError,
    InvalidSizeError,
    InvalidMinimumSizeError,
    InvalidMaximumSizeError,
    OverlappingBoundariesError,
    SingleMatchBoundariesError,
    UniquenessError,
    ItemValidationError,
)

from tests.utils import sample
from tests.strategies import (
    st_hashable,
    st_anything_except,
    st_anything_comparable,
    Draw,
)

MINIMUM_EXTREMUM: Final[Literal["minimum"]] = "minimum"
MAXIMUM_EXTREMUM: Final[Literal["maximum"]] = "maximum"

MINIMUM_ALLOWED_SIZE: Final[int] = 0
MAXIMUM_ALLOWED_SIZE: Final[int] = sys.maxsize


@st.composite
def st_size(
    draw: Draw[int],
    min_value: int = MINIMUM_ALLOWED_SIZE,
    max_value: int = MAXIMUM_ALLOWED_SIZE,
) -> int:
    return draw(st.integers(min_value=min_value, max_value=max_value))


@st.composite
def st_minimum(draw: Draw[int], size: int) -> int:
    return draw(st.integers(min_value=MINIMUM_ALLOWED_SIZE, max_value=size))


@st.composite
def st_maximum(draw: Draw[int], size: int) -> int:
    return draw(st.integers(min_value=size, max_value=MAXIMUM_ALLOWED_SIZE))


@st.composite
def st_size_below_minimum(draw: Draw[int]) -> int:
    below_minimum = draw(st.integers(max_value=MINIMUM_ALLOWED_SIZE))
    assume(below_minimum != MINIMUM_ALLOWED_SIZE)

    return below_minimum


@st.composite
def st_size_above_maximum(draw: Draw[int]) -> int:
    above_maximum = draw(st.integers(min_value=MAXIMUM_ALLOWED_SIZE))
    assume(above_maximum != MAXIMUM_ALLOWED_SIZE)

    return above_maximum


def test_repr() -> None:
    assert (validator_result := sequence_validator())

    fmt = "testplates.sequence_validator()"
    validator = unwrap_success(validator_result)
    assert repr(validator) == fmt


@given(data=st.lists(st_anything_comparable()))
def test_success(data: Sequence[Any]) -> None:
    assert (validator_result := sequence_validator())

    validator = unwrap_success(validator_result)
    assert (validation_result := validator(data))

    outcome = unwrap_success(validation_result)
    assert outcome is None


# noinspection PyTypeChecker
@given(st_data=st.data(), data=st.text())
def test_success_with_minimum_size(st_data: st.DataObject, data: str) -> None:
    size = len(data)

    minimum = st_data.draw(st_minimum(size))

    assert (validator_result := sequence_validator(minimum_size=minimum))

    validator = unwrap_success(validator_result)
    assert (validation_result := validator(data))

    outcome = unwrap_success(validation_result)
    assert outcome is None


# noinspection PyTypeChecker
@given(st_data=st.data(), data=st.text())
def test_success_with_maximum_size(st_data: st.DataObject, data: str) -> None:
    size = len(data)

    maximum = st_data.draw(st_maximum(size))

    assert (validator_result := sequence_validator(maximum_size=maximum))

    validator = unwrap_success(validator_result)
    assert (validation_result := validator(data))

    outcome = unwrap_success(validation_result)
    assert outcome is None


# noinspection PyTypeChecker
@given(st_data=st.data(), data=st.text())
def test_success_with_minimum_size_and_maximum_size(st_data: st.DataObject, data: str) -> None:
    size = len(data)

    minimum = st_data.draw(st_minimum(size))
    maximum = st_data.draw(st_maximum(size))

    assume(minimum != maximum)

    assert (validator_result := sequence_validator(minimum_size=minimum, maximum_size=maximum))

    validator = unwrap_success(validator_result)
    assert (validation_result := validator(data))

    outcome = unwrap_success(validation_result)
    assert outcome is None


@given(data=st.lists(st_hashable(), min_size=1, unique=True))
def test_success_with_unique_value(data: Sequence[Any]) -> None:
    assert (validator_result := sequence_validator(unique_items=True))

    validator = unwrap_success(validator_result)
    assert (validation_result := validator(data))

    outcome = unwrap_success(validation_result)
    assert outcome is None


def test_failure_when_item_validator_fails() -> None:
    validator_error = TestplatesError()
    assert not (validator_result := sequence_validator(failure(validator_error)))

    error = unwrap_failure(validator_result)
    assert error is validator_error


@given(data=st_anything_except(Sequence))
def test_failure_when_data_validation_fails(data: Any) -> None:
    assert (validator_result := sequence_validator())

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == (Sequence,)


# noinspection PyTypeChecker
@given(st_data=st.data(), data=st.text())
def test_failure_when_value_is_above_minimum_size_and_maximum_size(
    st_data: st.DataObject,
    data: str,
) -> None:
    size = len(data)

    minimum_size = st_data.draw(st_size(min_value=size))
    maximum_size = st_data.draw(st_size(min_value=minimum_size))

    assume(minimum_size != size)
    assume(minimum_size != maximum_size)

    assert (
        validator_result := sequence_validator(
            minimum_size=minimum_size,
            maximum_size=maximum_size,
        )
    )

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidMinimumSizeError)
    assert error.data == data
    assert error.minimum.value == minimum_size


# noinspection PyTypeChecker
@given(st_data=st.data(), data=st.text())
def test_failure_when_value_is_below_minimum_size_and_maximum_size(
    st_data: st.DataObject,
    data: str,
) -> None:
    size = len(data)

    maximum_size = st_data.draw(st_size(max_value=size))
    minimum_size = st_data.draw(st_size(max_value=maximum_size))

    assume(maximum_size != size)
    assume(minimum_size != maximum_size)

    assert (
        validator_result := sequence_validator(
            minimum_size=minimum_size,
            maximum_size=maximum_size,
        )
    )

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidMaximumSizeError)
    assert error.data == data
    assert error.maximum.value == maximum_size


# noinspection PyTypeChecker
@given(data=st.data(), size=st_size())
def test_failure_when_size_boundaries_are_below_zero(data: st.DataObject, size: int) -> None:
    below_minimum_size = data.draw(st_size_below_minimum())

    assert not (
        validator_result := sequence_validator(
            minimum_size=below_minimum_size,
            maximum_size=size,
        )
    )

    error = unwrap_failure(validator_result)
    assert isinstance(error, InvalidSizeError)
    assert error.boundary.value == below_minimum_size
    assert error.boundary.is_inclusive is True

    assert not (
        validator_result := sequence_validator(
            minimum_size=size,
            maximum_size=below_minimum_size,
        )
    )

    error = unwrap_failure(validator_result)
    assert isinstance(error, InvalidSizeError)
    assert error.boundary.value == below_minimum_size
    assert error.boundary.is_inclusive is True


# noinspection PyTypeChecker
@given(data=st.data(), size=st_size())
def test_failure_when_size_boundaries_are_above_max_size(data: st.DataObject, size: int) -> None:
    above_maximum_size = data.draw(st_size_above_maximum())

    assert not (
        validator_result := sequence_validator(
            minimum_size=above_maximum_size,
            maximum_size=size,
        )
    )

    error = unwrap_failure(validator_result)
    assert isinstance(error, InvalidSizeError)
    assert error.boundary.value == above_maximum_size
    assert error.boundary.is_inclusive is True

    assert not (
        validator_result := sequence_validator(
            minimum_size=size,
            maximum_size=above_maximum_size,
        )
    )

    error = unwrap_failure(validator_result)
    assert isinstance(error, InvalidSizeError)
    assert error.boundary.value == above_maximum_size
    assert error.boundary.is_inclusive is True


# noinspection PyTypeChecker
@given(data=st.data())
def test_failure_when_size_boundaries_are_overlapping(data: st.DataObject) -> None:
    minimum_size = data.draw(st_size())
    maximum_size = data.draw(st_size(max_value=minimum_size))

    assume(minimum_size != maximum_size)

    assert not (
        validator_result := sequence_validator(
            minimum_size=minimum_size,
            maximum_size=maximum_size,
        )
    )

    error = unwrap_failure(validator_result)
    assert isinstance(error, OverlappingBoundariesError)
    assert error.minimum.value == minimum_size
    assert error.minimum.is_inclusive is True
    assert error.maximum.value == maximum_size
    assert error.maximum.is_inclusive is True


# noinspection PyTypeChecker
@given(size=st_size())
def test_failure_when_size_boundaries_match_single_value(size: int) -> None:
    assert not (validator_result := sequence_validator(minimum_size=size, maximum_size=size))

    error = unwrap_failure(validator_result)
    assert isinstance(error, SingleMatchBoundariesError)
    assert error.minimum.value == size
    assert error.minimum.is_inclusive is True
    assert error.maximum.value == size
    assert error.maximum.is_inclusive is True


@given(data=st.lists(st_hashable(), min_size=1, unique=True))
def test_failure_when_value_is_not_unique(data: List[Hashable]) -> None:
    data.append(sample(data))

    assert (validator_result := sequence_validator(unique_items=True))

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

    assert (validator_result := sequence_validator(success(validator)))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator([value]))

    error = unwrap_failure(validation_result)
    assert isinstance(error, ItemValidationError)
    assert error.data == [value]
    assert error.item == value
    assert error.error == item_error
