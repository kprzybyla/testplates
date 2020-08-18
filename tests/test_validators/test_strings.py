import re

from typing import TypeVar, List, Final

import pytest

from resultful import unwrap_success, unwrap_failure
from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import UNLIMITED
from testplates import string_validator, bytes_validator
from testplates import (
    InvalidTypeError,
    InvalidMinimumSizeError,
    InvalidMaximumSizeError,
    InvalidFormatError,
)

from tests.strategies import st_anything_except, Draw

_T = TypeVar("_T")

ANY_WORD: Final[str] = r"\w+"
ANY_DIGIT: Final[str] = r"\d+"
MAC_ADDRESS: Final[str] = r"([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})"
HEX_COLOR_NUMBER: Final[str] = r"\B#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})\b"

STR_PATTERNS: Final[List[str]] = [ANY_WORD, ANY_DIGIT, MAC_ADDRESS, HEX_COLOR_NUMBER]
BYTES_PATTERNS: Final[List[bytes]] = list(map(str.encode, STR_PATTERNS))

# TODO(kprzybyla): Implement generic st_from_pattern after following issue is resolved:
#                  https://github.com/HypothesisWorks/hypothesis/issues/2365


@st.composite
def st_from_str_pattern(draw: Draw[str], pattern: str) -> str:
    return draw(st.from_regex(pattern, fullmatch=True))


@st.composite
def st_from_bytes_pattern(draw: Draw[bytes], pattern: bytes) -> bytes:
    return draw(st.from_regex(pattern, fullmatch=True))


@st.composite
def st_from_str_pattern_inverse(draw: Draw[str], pattern: str) -> str:
    text = draw(st.text())
    assume(not re.match(pattern, text))

    return text


@st.composite
def st_from_bytes_pattern_inverse(draw: Draw[bytes], pattern: bytes) -> bytes:
    binary = draw(st.binary())
    assume(not re.match(pattern, binary))

    return binary


def test_repr_str() -> None:
    assert (validator_result := string_validator(minimum_size=UNLIMITED, maximum_size=UNLIMITED))

    fmt = "testplates.string_validator()"
    validator = unwrap_success(validator_result)
    assert repr(validator) == fmt


def test_repr_bytes() -> None:
    assert (validator_result := bytes_validator(minimum_size=UNLIMITED, maximum_size=UNLIMITED))

    fmt = "testplates.bytes_validator()"
    validator = unwrap_success(validator_result)
    assert repr(validator) == fmt


@given(data=st.text())
def test_success_str(data: str) -> None:
    assert (validator_result := string_validator(minimum_size=UNLIMITED, maximum_size=UNLIMITED))

    validator = unwrap_success(validator_result)
    assert (validation_result := validator(data))

    outcome = unwrap_success(validation_result)
    assert outcome is None


# noinspection PyTypeChecker
@given(st_data=st.data())
@pytest.mark.parametrize("pattern", STR_PATTERNS)
def test_success_str_with_pattern(st_data: st.DataObject, pattern: str) -> None:
    data = st_data.draw(st_from_str_pattern(pattern))

    assert (
        validator_result := string_validator(
            minimum_size=UNLIMITED, maximum_size=UNLIMITED, pattern=pattern
        )
    )

    validator = unwrap_success(validator_result)
    assert (validation_result := validator(data))

    outcome = unwrap_success(validation_result)
    assert outcome is None


@given(data=st.binary())
def test_success_bytes(data: bytes) -> None:
    assert (validator_result := bytes_validator(minimum_size=UNLIMITED, maximum_size=UNLIMITED))

    validator = unwrap_success(validator_result)
    assert (validation_result := validator(data))

    outcome = unwrap_success(validation_result)
    assert outcome is None


# noinspection PyTypeChecker
@given(st_data=st.data())
@pytest.mark.parametrize("pattern", BYTES_PATTERNS)
def test_success_bytes_with_pattern(st_data: st.DataObject, pattern: bytes) -> None:
    data = st_data.draw(st_from_bytes_pattern(pattern))

    assert (
        validator_result := bytes_validator(
            minimum_size=UNLIMITED, maximum_size=UNLIMITED, pattern=pattern
        )
    )

    validator = unwrap_success(validator_result)
    assert (validation_result := validator(data))

    outcome = unwrap_success(validation_result)
    assert outcome is None


@given(data=st_anything_except(str))
def test_failure_str_when_data_validation_fails(data: _T) -> None:
    assert (validator_result := string_validator(minimum_size=UNLIMITED, maximum_size=UNLIMITED))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == (str,)


@given(data=st_anything_except(bytes))
def test_failure_bytes_when_data_validation_fails(data: _T) -> None:
    assert (validator_result := bytes_validator(minimum_size=UNLIMITED, maximum_size=UNLIMITED))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidTypeError)
    assert error.data == data
    assert error.allowed_types == (bytes,)


@given(st_data=st.data(), data=st.text())
def test_failure_str_when_value_does_not_fit_minimum_value(
    st_data: st.DataObject, data: str
) -> None:
    minimum = st_data.draw(st.integers(min_value=len(data)))

    assume(len(data) < minimum)

    assert (validator_result := string_validator(minimum_size=minimum, maximum_size=UNLIMITED))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidMinimumSizeError)
    assert error.data == data
    assert error.minimum.value == minimum


@given(st_data=st.data(), data=st.text())
def test_failure_str_when_value_does_not_fit_maximum_value(
    st_data: st.DataObject, data: str
) -> None:
    maximum = st_data.draw(st.integers(max_value=len(data)))

    assume(len(data) > maximum)

    assert (validator_result := string_validator(minimum_size=UNLIMITED, maximum_size=maximum))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidMaximumSizeError)
    assert error.data == data
    assert error.maximum.value == maximum


@given(st_data=st.data(), data=st.binary())
def test_failure_bytes_when_value_does_not_fit_minimum_value(
    st_data: st.DataObject, data: bytes
) -> None:
    minimum = st_data.draw(st.integers(min_value=len(data)))

    assume(len(data) < minimum)

    assert (validator_result := bytes_validator(minimum_size=minimum, maximum_size=UNLIMITED))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidMinimumSizeError)
    assert error.data == data
    assert error.minimum.value == minimum


@given(st_data=st.data(), data=st.binary())
def test_failure_bytes_when_value_does_not_fit_maximum_value(
    st_data: st.DataObject, data: bytes
) -> None:
    maximum = st_data.draw(st.integers(max_value=len(data)))

    assume(len(data) > maximum)

    assert (validator_result := bytes_validator(minimum_size=UNLIMITED, maximum_size=maximum))

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidMaximumSizeError)
    assert error.data == data
    assert error.maximum.value == maximum


# noinspection PyTypeChecker
@given(st_data=st.data())
@pytest.mark.parametrize("pattern", STR_PATTERNS)
def test_failure_str_when_value_does_not_pattern(st_data: st.DataObject, pattern: str) -> None:
    data = st_data.draw(st_from_str_pattern_inverse(pattern))

    assert (
        validator_result := string_validator(
            minimum_size=UNLIMITED, maximum_size=UNLIMITED, pattern=pattern
        )
    )

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidFormatError)
    assert error.data == data
    assert error.pattern.pattern == pattern


# noinspection PyTypeChecker
@given(st_data=st.data())
@pytest.mark.parametrize("pattern", BYTES_PATTERNS)
def test_failure_bytes_when_value_does_not_pattern(st_data: st.DataObject, pattern: bytes) -> None:
    data = st_data.draw(st_from_bytes_pattern_inverse(pattern))

    assert (
        validator_result := bytes_validator(
            minimum_size=UNLIMITED, maximum_size=UNLIMITED, pattern=pattern
        )
    )

    validator = unwrap_success(validator_result)
    assert not (validation_result := validator(data))

    error = unwrap_failure(validation_result)
    assert isinstance(error, InvalidFormatError)
    assert error.data == data
    assert error.pattern.pattern == pattern
