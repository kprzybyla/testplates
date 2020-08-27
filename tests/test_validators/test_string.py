import re
import sys

from typing import (
    TypeVar,
    List,
    Literal,
    Final,
)

import pytest

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
    string_validator,
    InvalidTypeError,
    InvalidSizeError,
    InvalidMinimumSizeError,
    InvalidMaximumSizeError,
    OverlappingBoundariesError,
    SingleMatchBoundariesError,
    InvalidFormatError,
)

from tests.strategies import (
    st_anything_except,
    Draw,
)

_T = TypeVar("_T")

MINIMUM_EXTREMUM: Final[Literal["minimum"]] = "minimum"
MAXIMUM_EXTREMUM: Final[Literal["maximum"]] = "maximum"

MINIMUM_ALLOWED_SIZE: Final[int] = 0
MAXIMUM_ALLOWED_SIZE: Final[int] = sys.maxsize

ANY_WORD: Final[str] = r"\w+"
ANY_DIGIT: Final[str] = r"\d+"
MAC_ADDRESS: Final[str] = r"([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})"
HEX_COLOR_NUMBER: Final[str] = r"\B#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})\b"

STR_PATTERNS: Final[List[str]] = [
    ANY_WORD,
    ANY_DIGIT,
    MAC_ADDRESS,
    HEX_COLOR_NUMBER,
]


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


@st.composite
def st_from_pattern(draw: Draw[str], pattern: str) -> str:
    return draw(st.from_regex(pattern, fullmatch=True))


@st.composite
def st_from_pattern_inverse(draw: Draw[str], pattern: str) -> str:
    text = draw(st.text())
    assume(not re.match(pattern, text))

    return text


def test_repr() -> None:
    assert (validator_result := string_validator())

    fmt = "testplates.string_validator()"
    validator = unwrap_success(validator_result)
    assert repr(validator) == fmt


@given(data=st.text())
def test_success(data: str) -> None:
    assert (validator_result := string_validator())

    validator = unwrap_success(validator_result)
    assert (validation_result := validator(data))

    outcome = unwrap_success(validation_result)
    assert outcome is None


# noinspection PyTypeChecker
@given(st_data=st.data(), data=st.text())
def test_success_with_minimum_size(st_data: st.DataObject, data: str) -> None:
    size = len(data)

    minimum = st_data.draw(st_minimum(size))

    assert (validator_result := string_validator(minimum_size=minimum))

    validator = unwrap_success(validator_result)
    assert (validation_result := validator(data))

    outcome = unwrap_success(validation_result)
    assert outcome is None


# noinspection PyTypeChecker
@given(st_data=st.data(), data=st.text())
def test_success_with_maximum_size(st_data: st.DataObject, data: str) -> None:
    size = len(data)

    maximum = st_data.draw(st_maximum(size))

    assert (validator_result := string_validator(maximum_size=maximum))

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

    assert (validator_result := string_validator(minimum_size=minimum, maximum_size=maximum))

    validator = unwrap_success(validator_result)
    assert (validation_result := validator(data))

    outcome = unwrap_success(validation_result)
    assert outcome is None


# noinspection PyTypeChecker
@given(st_data=st.data())
@pytest.mark.parametrize("pattern", STR_PATTERNS)
def test_success_with_pattern(st_data: st.DataObject, pattern: str) -> None:
    data = st_data.draw(st_from_pattern(pattern))

    assert (validator_result := string_validator(pattern=pattern))

    validator = unwrap_success(validator_result)
    assert (validation_result := validator(data))

    outcome = unwrap_success(validation_result)
    assert outcome is None


@given(data=st_anything_except(str))
def test_failure_when_data_validation_fails(data: _T) -> None:
    assert (validator_result := string_validator())

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == (str,)


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
        validator_result := string_validator(
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
        validator_result := string_validator(
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
        validator_result := string_validator(
            minimum_size=below_minimum_size,
            maximum_size=size,
        )
    )

    error = unwrap_failure(validator_result)
    assert isinstance(error, InvalidSizeError)
    assert error.boundary.value == below_minimum_size
    assert error.boundary.is_inclusive is True

    assert not (
        validator_result := string_validator(
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
        validator_result := string_validator(
            minimum_size=above_maximum_size,
            maximum_size=size,
        )
    )

    error = unwrap_failure(validator_result)
    assert isinstance(error, InvalidSizeError)
    assert error.boundary.value == above_maximum_size
    assert error.boundary.is_inclusive is True

    assert not (
        validator_result := string_validator(
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
        validator_result := string_validator(
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
    assert not (validator_result := string_validator(minimum_size=size, maximum_size=size))

    error = unwrap_failure(validator_result)
    assert isinstance(error, SingleMatchBoundariesError)
    assert error.minimum.value == size
    assert error.minimum.is_inclusive is True
    assert error.maximum.value == size
    assert error.maximum.is_inclusive is True


# noinspection PyTypeChecker
@given(st_data=st.data())
@pytest.mark.parametrize("pattern", STR_PATTERNS)
def test_failure_when_value_does_not_pattern(st_data: st.DataObject, pattern: str) -> None:
    data = st_data.draw(st_from_pattern_inverse(pattern))

    assert (validator_result := string_validator(pattern=pattern))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidFormatError)
    assert error.data == data
    assert error.pattern.pattern == pattern
