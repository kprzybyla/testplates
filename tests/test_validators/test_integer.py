from typing import (
    Any,
    Optional,
    Literal,
    Final,
)

from resultful import (
    unwrap_success,
    unwrap_failure,
)

from hypothesis import (
    assume,
    given,
    strategies as st,
)

from testplates import (
    integer_validator,
    InvalidTypeError,
    ProhibitedBoolValueError,
    InvalidMinimumValueError,
    InvalidMaximumValueError,
    MutuallyExclusiveBoundariesError,
    OverlappingBoundariesError,
    SingleMatchBoundariesError,
)

from tests.strategies import (
    st_anything_except,
    Draw,
)

MINIMUM_EXTREMUM: Final[Literal["minimum"]] = "minimum"
MAXIMUM_EXTREMUM: Final[Literal["maximum"]] = "maximum"

EXCLUSIVE_ALIGNMENT: Final[int] = 1


@st.composite
def st_value(
    draw: Draw[int],
    min_value: Optional[int] = None,
    max_value: Optional[int] = None,
) -> int:
    return draw(st.integers(min_value=min_value, max_value=max_value))


@st.composite
def st_inclusive_minimum(draw: Draw[int], value: int) -> int:
    return draw(st.integers(max_value=value))


@st.composite
def st_inclusive_maximum(draw: Draw[int], value: int) -> int:
    return draw(st.integers(min_value=value))


@st.composite
def st_exclusive_minimum(draw: Draw[int], value: int) -> int:
    minimum = draw(st_inclusive_minimum(value))
    assume(value != minimum)

    return minimum


@st.composite
def st_exclusive_maximum(draw: Draw[int], value: int) -> int:
    maximum = draw(st_inclusive_maximum(value))
    assume(value != maximum)

    return maximum


def test_repr() -> None:
    assert (validator_result := integer_validator())

    fmt = "testplates.integer_validator()"
    validator = unwrap_success(validator_result)
    assert repr(validator) == fmt.format()


@given(data=st.booleans())
def test_success_when_allow_bool_is_true(data: bool) -> None:
    assert (validator_result := integer_validator(allow_bool=True))

    validator = unwrap_success(validator_result)
    assert (validation_result := validator(data))

    outcome = unwrap_success(validation_result)
    assert outcome is None


@given(data=st_anything_except(int))
def test_failure_when_data_type_validation_fails(data: Any) -> None:
    assert (validator_result := integer_validator())

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == (int,)


@given(data=st.booleans())
def test_failure_when_allow_bool_is_false(data: bool) -> None:
    assert (validator_result := integer_validator())

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, ProhibitedBoolValueError)
    assert error.data == data


@given(st_data=st.data(), data=st.integers())
def test_failure_when_value_does_not_fit_minimum_value(st_data: st.DataObject, data: int) -> None:
    minimum = st_data.draw(st.integers(min_value=data))

    assume(data < minimum)

    assert (validator_result := integer_validator(minimum=minimum))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidMinimumValueError)
    assert error.data == data
    assert error.minimum.value == minimum


@given(st_data=st.data(), data=st.integers())
def test_failure_when_value_does_not_fit_maximum_value(st_data: st.DataObject, data: int) -> None:
    maximum = st_data.draw(st.integers(max_value=data))

    assume(data > maximum)

    assert (validator_result := integer_validator(maximum=maximum))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidMaximumValueError)
    assert error.data == data
    assert error.maximum.value == maximum


# noinspection PyTypeChecker
@given(data=st_value())
def test_success_with_unlimited_minimum_and_unlimited_maximum(data: int) -> None:
    assert (validator_result := integer_validator())

    validator = unwrap_success(validator_result)
    assert (validation_result := validator(data))

    outcome = unwrap_success(validation_result)
    assert outcome is None


# noinspection PyTypeChecker
@given(st_data=st.data(), data=st_value())
def test_success_with_inclusive_minimum_and_inclusive_maximum(
    st_data: st.DataObject,
    data: int,
) -> None:
    inclusive_minimum = st_data.draw(st_inclusive_minimum(data))
    inclusive_maximum = st_data.draw(st_inclusive_maximum(data))

    assume(inclusive_minimum != inclusive_maximum)

    assert (
        validator_result := integer_validator(
            minimum=inclusive_minimum,
            maximum=inclusive_maximum,
        )
    )

    validator = unwrap_success(validator_result)
    assert (validation_result := validator(data))

    outcome = unwrap_success(validation_result)
    assert outcome is None


# noinspection PyTypeChecker
@given(st_data=st.data(), data=st_value())
def test_success_with_inclusive_minimum_and_exclusive_maximum(
    st_data: st.DataObject,
    data: int,
) -> None:
    inclusive_minimum = st_data.draw(st_inclusive_minimum(data))
    exclusive_maximum = st_data.draw(st_exclusive_maximum(data))

    assume(inclusive_minimum != exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    assert (
        validator_result := integer_validator(
            minimum=inclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    validator = unwrap_success(validator_result)
    assert (validation_result := validator(data))

    outcome = unwrap_success(validation_result)
    assert outcome is None


# noinspection PyTypeChecker
@given(st_data=st.data(), data=st_value())
def test_success_with_exclusive_minimum_and_inclusive_maximum(
    st_data: st.DataObject,
    data: int,
) -> None:
    exclusive_minimum = st_data.draw(st_exclusive_minimum(data))
    inclusive_maximum = st_data.draw(st_inclusive_maximum(data))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT != inclusive_maximum)

    assert (
        validator_result := integer_validator(
            exclusive_minimum=exclusive_minimum,
            maximum=inclusive_maximum,
        )
    )

    validator = unwrap_success(validator_result)
    assert (validation_result := validator(data))

    outcome = unwrap_success(validation_result)
    assert outcome is None


# noinspection PyTypeChecker
@given(st_data=st.data(), data=st_value())
def test_success_with_exclusive_minimum_and_exclusive_maximum(
    st_data: st.DataObject,
    data: int,
) -> None:
    exclusive_minimum = st_data.draw(st_exclusive_minimum(data))
    exclusive_maximum = st_data.draw(st_exclusive_maximum(data))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT != exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    assert (
        validator_result := integer_validator(
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    validator = unwrap_success(validator_result)
    assert (validation_result := validator(data))

    outcome = unwrap_success(validation_result)
    assert outcome is None


# noinspection PyTypeChecker
@given(st_data=st.data(), data=st_value())
def test_failure_when_value_is_above_inclusive_minimum_and_inclusive_maximum(
    st_data: st.DataObject,
    data: int,
) -> None:
    inclusive_maximum = st_data.draw(st_value(max_value=data))
    inclusive_minimum = st_data.draw(st_value(max_value=inclusive_maximum))

    assume(inclusive_maximum != data)
    assume(inclusive_minimum != inclusive_maximum)

    assert (
        validator_result := integer_validator(
            minimum=inclusive_minimum,
            maximum=inclusive_maximum,
        )
    )

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidMaximumValueError)
    assert error.data == data
    assert error.maximum.value == inclusive_maximum


# noinspection PyTypeChecker
@given(st_data=st.data(), data=st_value())
def test_failure_when_value_is_below_inclusive_minimum_and_inclusive_maximum(
    st_data: st.DataObject,
    data: int,
) -> None:
    inclusive_minimum = st_data.draw(st_value(min_value=data))
    inclusive_maximum = st_data.draw(st_value(min_value=inclusive_minimum))

    assume(inclusive_minimum != data)
    assume(inclusive_minimum != inclusive_maximum)

    assert (
        validator_result := integer_validator(
            minimum=inclusive_minimum,
            maximum=inclusive_maximum,
        )
    )

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidMinimumValueError)
    assert error.data == data
    assert error.minimum.value == inclusive_minimum


# noinspection PyTypeChecker
@given(st_data=st.data(), data=st_value())
def test_failure_when_value_is_above_inclusive_minimum_and_exclusive_maximum(
    st_data: st.DataObject,
    data: int,
) -> None:
    exclusive_maximum = st_data.draw(st_value(max_value=data))
    inclusive_minimum = st_data.draw(st_value(max_value=exclusive_maximum))

    assume(inclusive_minimum < exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    assert (
        validator_result := integer_validator(
            minimum=inclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidMaximumValueError)
    assert error.data == data
    assert error.maximum.value == exclusive_maximum


# noinspection PyTypeChecker
@given(st_data=st.data(), data=st_value())
def test_failure_when_value_is_below_inclusive_minimum_and_exclusive_maximum(
    st_data: st.DataObject,
    data: int,
) -> None:
    inclusive_minimum = st_data.draw(st_value(min_value=data))
    exclusive_maximum = st_data.draw(st_value(min_value=inclusive_minimum))

    assume(inclusive_minimum != data)
    assume(inclusive_minimum < exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    assert (
        validator_result := integer_validator(
            minimum=inclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidMinimumValueError)
    assert error.data == data
    assert error.minimum.value == inclusive_minimum


# noinspection PyTypeChecker
@given(st_data=st.data(), data=st_value())
def test_failure_when_value_is_above_exclusive_minimum_and_inclusive_maximum(
    st_data: st.DataObject,
    data: int,
) -> None:
    inclusive_maximum = st_data.draw(st_value(max_value=data))
    exclusive_minimum = st_data.draw(st_value(max_value=inclusive_maximum))

    assume(inclusive_maximum != data)
    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT < inclusive_maximum)

    assert (
        validator_result := integer_validator(
            exclusive_minimum=exclusive_minimum,
            maximum=inclusive_maximum,
        )
    )

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidMaximumValueError)
    assert error.data == data
    assert error.maximum.value == inclusive_maximum


# noinspection PyTypeChecker
@given(st_data=st.data(), data=st_value())
def test_failure_when_value_is_below_exclusive_minimum_and_inclusive_maximum(
    st_data: st.DataObject,
    data: int,
) -> None:
    exclusive_minimum = st_data.draw(st_value(min_value=data))
    inclusive_maximum = st_data.draw(st_value(min_value=exclusive_minimum))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT < inclusive_maximum)

    assert (
        validator_result := integer_validator(
            exclusive_minimum=exclusive_minimum,
            maximum=inclusive_maximum,
        )
    )

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidMinimumValueError)
    assert error.data == data
    assert error.minimum.value == exclusive_minimum


# noinspection PyTypeChecker
@given(st_data=st.data(), data=st_value())
def test_failure_when_value_is_above_exclusive_minimum_and_exclusive_maximum(
    st_data: st.DataObject,
    data: int,
) -> None:
    exclusive_maximum = st_data.draw(st_value(max_value=data))
    exclusive_minimum = st_data.draw(st_value(max_value=exclusive_maximum))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT < exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    assert (
        validator_result := integer_validator(
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidMaximumValueError)
    assert error.data == data
    assert error.maximum.value == exclusive_maximum


# noinspection PyTypeChecker
@given(st_data=st.data(), data=st_value())
def test_failure_when_value_is_below_exclusive_minimum_and_exclusive_maximum(
    st_data: st.DataObject,
    data: int,
) -> None:
    exclusive_minimum = st_data.draw(st_value(min_value=data))
    exclusive_maximum = st_data.draw(st_value(min_value=exclusive_minimum))

    assume(exclusive_minimum + EXCLUSIVE_ALIGNMENT < exclusive_maximum - EXCLUSIVE_ALIGNMENT)

    assert (
        validator_result := integer_validator(
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidMinimumValueError)
    assert error.data == data
    assert error.minimum.value == exclusive_minimum


# noinspection PyTypeChecker
# noinspection PyArgumentList
@given(st_data=st.data(), data=st_value())
def test_failure_when_mutually_exclusive_boundaries_are_set(
    st_data: st.DataObject,
    data: int,
) -> None:
    inclusive_minimum = st_data.draw(st_inclusive_minimum(data))
    inclusive_maximum = st_data.draw(st_inclusive_maximum(data))

    exclusive_minimum = st_data.draw(st_exclusive_minimum(data))
    exclusive_maximum = st_data.draw(st_exclusive_maximum(data))

    assert not (
        validator_result := integer_validator(
            minimum=inclusive_minimum,
            maximum=inclusive_maximum,
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    error = unwrap_failure(validator_result)
    assert isinstance(error, MutuallyExclusiveBoundariesError)
    assert error.name == MINIMUM_EXTREMUM


# noinspection PyTypeChecker
# noinspection PyArgumentList
@given(st_data=st.data(), data=st_value())
def test_failure_when_mutually_exclusive_minimum_boundaries_are_set(
    st_data: st.DataObject,
    data: int,
) -> None:
    inclusive_minimum = st_data.draw(st_inclusive_minimum(data))
    inclusive_maximum = st_data.draw(st_inclusive_maximum(data))

    exclusive_minimum = st_data.draw(st_exclusive_minimum(data))
    exclusive_maximum = st_data.draw(st_exclusive_maximum(data))

    assert not (
        validator_result := integer_validator(
            minimum=inclusive_minimum,
            maximum=inclusive_maximum,
            exclusive_minimum=exclusive_minimum,
        )
    )

    error = unwrap_failure(validator_result)
    assert isinstance(error, MutuallyExclusiveBoundariesError)
    assert error.name == MINIMUM_EXTREMUM

    assert not (
        validator_result := integer_validator(
            minimum=inclusive_minimum,
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    error = unwrap_failure(validator_result)
    assert isinstance(error, MutuallyExclusiveBoundariesError)
    assert error.name == MINIMUM_EXTREMUM


# noinspection PyTypeChecker
# noinspection PyArgumentList
@given(st_data=st.data(), data=st_value())
def test_failure_when_mutually_exclusive_maximum_boundaries_are_set(
    st_data: st.DataObject,
    data: int,
) -> None:
    inclusive_minimum = st_data.draw(st_inclusive_minimum(data))
    inclusive_maximum = st_data.draw(st_inclusive_maximum(data))

    exclusive_minimum = st_data.draw(st_exclusive_minimum(data))
    exclusive_maximum = st_data.draw(st_exclusive_maximum(data))

    assert not (
        validator_result := integer_validator(
            minimum=inclusive_minimum,
            maximum=inclusive_maximum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    error = unwrap_failure(validator_result)
    assert isinstance(error, MutuallyExclusiveBoundariesError)
    assert error.name == MAXIMUM_EXTREMUM

    assert not (
        validator_result := integer_validator(
            maximum=inclusive_maximum,
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    error = unwrap_failure(validator_result)
    assert isinstance(error, MutuallyExclusiveBoundariesError)
    assert error.name == MAXIMUM_EXTREMUM


# noinspection PyTypeChecker
@given(st_data=st.data())
def test_failure_when_inclusive_minimum_and_inclusive_maximum_are_overlapping(
    st_data: st.DataObject,
) -> None:
    inclusive_minimum = st_data.draw(st_value())
    inclusive_maximum = st_data.draw(st_value(max_value=inclusive_minimum))

    assume(inclusive_minimum != inclusive_maximum)

    assert not (
        validator_result := integer_validator(
            minimum=inclusive_minimum,
            maximum=inclusive_maximum,
        )
    )

    error = unwrap_failure(validator_result)
    assert isinstance(error, OverlappingBoundariesError)
    assert error.minimum.value == inclusive_minimum
    assert error.minimum.is_inclusive is True
    assert error.maximum.value == inclusive_maximum
    assert error.maximum.is_inclusive is True


# noinspection PyTypeChecker
@given(st_data=st.data())
def test_failure_when_inclusive_minimum_and_exclusive_maximum_are_overlapping(
    st_data: st.DataObject,
) -> None:
    inclusive_minimum = st_data.draw(st_value())
    exclusive_maximum = st_data.draw(st_value(max_value=inclusive_minimum))

    assert not (
        validator_result := integer_validator(
            minimum=inclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    error = unwrap_failure(validator_result)
    assert isinstance(error, OverlappingBoundariesError)
    assert error.minimum.value == inclusive_minimum
    assert error.minimum.is_inclusive is True
    assert error.maximum.value == exclusive_maximum
    assert error.maximum.is_inclusive is False


# noinspection PyTypeChecker
@given(st_data=st.data())
def test_failure_when_exclusive_minimum_and_inclusive_maximum_are_overlapping(
    st_data: st.DataObject,
) -> None:
    exclusive_minimum = st_data.draw(st_value())
    inclusive_maximum = st_data.draw(st_value(max_value=exclusive_minimum))

    assert not (
        validator_result := integer_validator(
            exclusive_minimum=exclusive_minimum,
            maximum=inclusive_maximum,
        )
    )

    error = unwrap_failure(validator_result)
    assert isinstance(error, OverlappingBoundariesError)
    assert error.minimum.value == exclusive_minimum
    assert error.minimum.is_inclusive is False
    assert error.maximum.value == inclusive_maximum
    assert error.maximum.is_inclusive is True


# noinspection PyTypeChecker
@given(st_data=st.data())
def test_failure_when_exclusive_minimum_and_exclusive_maximum_are_overlapping(
    st_data: st.DataObject,
) -> None:
    exclusive_minimum = st_data.draw(st_value())
    exclusive_maximum = st_data.draw(st_value(max_value=exclusive_minimum + EXCLUSIVE_ALIGNMENT))

    assert not (
        validator_result := integer_validator(
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    error = unwrap_failure(validator_result)
    assert isinstance(error, OverlappingBoundariesError)
    assert error.minimum.value == exclusive_minimum
    assert error.minimum.is_inclusive is False
    assert error.maximum.value == exclusive_maximum
    assert error.maximum.is_inclusive is False


# noinspection PyTypeChecker
@given(data=st_value())
def test_failure_when_inclusive_minimum_and_inclusive_maximum_match_single_value(
    data: int,
) -> None:
    inclusive_minimum = data
    inclusive_maximum = data

    assert not (
        validator_result := integer_validator(
            minimum=inclusive_minimum,
            maximum=inclusive_maximum,
        )
    )

    error = unwrap_failure(validator_result)
    assert isinstance(error, SingleMatchBoundariesError)
    assert error.minimum.value == inclusive_minimum
    assert error.minimum.is_inclusive is True
    assert error.maximum.value == inclusive_maximum
    assert error.maximum.is_inclusive is True


# noinspection PyTypeChecker
@given(data=st_value())
def test_failure_when_inclusive_minimum_and_exclusive_maximum_match_single_value(
    data: int,
) -> None:
    inclusive_minimum = data
    exclusive_maximum = data + EXCLUSIVE_ALIGNMENT

    assert not (
        validator_result := integer_validator(
            minimum=inclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    error = unwrap_failure(validator_result)
    assert isinstance(error, SingleMatchBoundariesError)
    assert error.minimum.value == inclusive_minimum
    assert error.minimum.is_inclusive is True
    assert error.maximum.value == exclusive_maximum
    assert error.maximum.is_inclusive is False


# noinspection PyTypeChecker
@given(data=st_value())
def test_failure_when_exclusive_minimum_and_inclusive_maximum_match_single_value(
    data: int,
) -> None:
    exclusive_minimum = data - EXCLUSIVE_ALIGNMENT
    inclusive_maximum = data

    assert not (
        validator_result := integer_validator(
            exclusive_minimum=exclusive_minimum,
            maximum=inclusive_maximum,
        )
    )

    error = unwrap_failure(validator_result)
    assert isinstance(error, SingleMatchBoundariesError)
    assert error.minimum.value == exclusive_minimum
    assert error.minimum.is_inclusive is False
    assert error.maximum.value == inclusive_maximum
    assert error.maximum.is_inclusive is True


# noinspection PyTypeChecker
@given(data=st_value())
def test_failure_when_exclusive_minimum_and_exclusive_maximum_match_single_value(
    data: int,
) -> None:
    exclusive_minimum = data - EXCLUSIVE_ALIGNMENT
    exclusive_maximum = data + EXCLUSIVE_ALIGNMENT
    assert not (
        validator_result := integer_validator(
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    error = unwrap_failure(validator_result)
    assert isinstance(error, SingleMatchBoundariesError)
    assert error.minimum.value == exclusive_minimum
    assert error.minimum.is_inclusive is False
    assert error.maximum.value == exclusive_maximum
    assert error.maximum.is_inclusive is False
