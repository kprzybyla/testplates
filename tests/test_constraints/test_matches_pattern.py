import re

from typing import AnyStr, List, Union, Final

import pytest

from resultful import unwrap_success
from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import matches_pattern

from tests.strategies import Draw

ANY_WORD: Final[str] = r"\w+"
ANY_DIGIT: Final[str] = r"\d+"
MAC_ADDRESS: Final[str] = r"([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})"
HEX_COLOR_NUMBER: Final[str] = r"\B#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})\b"

STR_PATTERNS: Final[List[str]] = [ANY_WORD, ANY_DIGIT, MAC_ADDRESS, HEX_COLOR_NUMBER]
BYTES_PATTERNS: Final[List[bytes]] = list(map(str.encode, STR_PATTERNS))

PATTERNS: Final[List[Union[str, bytes]]] = [*STR_PATTERNS, *BYTES_PATTERNS]

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


@pytest.mark.parametrize("pattern", PATTERNS)
def test_repr(pattern: AnyStr) -> None:
    fmt = "testplates.matches_pattern({pattern})"

    assert (result := matches_pattern(pattern))

    constraint = unwrap_success(result)
    assert repr(constraint) == fmt.format(pattern=repr(pattern))


# noinspection PyTypeChecker
@given(data=st.data())
@pytest.mark.parametrize("pattern", STR_PATTERNS)
def test_returns_true_with_str_pattern(data: st.DataObject, pattern: str) -> None:
    value = data.draw(st_from_str_pattern(pattern))

    assert (result := matches_pattern(pattern))

    constraint = unwrap_success(result)
    assert constraint == value


# noinspection PyTypeChecker
@given(data=st.data())
@pytest.mark.parametrize("pattern", BYTES_PATTERNS)
def test_returns_true_with_bytes_pattern(data: st.DataObject, pattern: bytes) -> None:
    value = data.draw(st_from_bytes_pattern(pattern))

    assert (result := matches_pattern(pattern))

    constraint = unwrap_success(result)
    assert constraint == value


# noinspection PyTypeChecker
@given(data=st.data())
@pytest.mark.parametrize("pattern", STR_PATTERNS)
def test_returns_false_with_str_pattern(data: st.DataObject, pattern: str) -> None:
    value = data.draw(st_from_str_pattern_inverse(pattern))

    assert (result := matches_pattern(pattern))

    constraint = unwrap_success(result)
    assert constraint != value


# noinspection PyTypeChecker
@given(data=st.data())
@pytest.mark.parametrize("pattern", BYTES_PATTERNS)
def test_returns_false_with_bytes_pattern(data: st.DataObject, pattern: bytes) -> None:
    value = data.draw(st_from_bytes_pattern_inverse(pattern))

    assert (result := matches_pattern(pattern))

    constraint = unwrap_success(result)
    assert constraint != value


# noinspection PyTypeChecker
@given(data=st.data())
@pytest.mark.parametrize("pattern", STR_PATTERNS)
def test_returns_false_with_str_pattern_and_bytes_value(data: st.DataObject, pattern: str) -> None:
    value = data.draw(st_from_str_pattern(pattern))

    assert (result := matches_pattern(pattern))

    constraint = unwrap_success(result)
    assert constraint != value.encode()


# noinspection PyTypeChecker
@given(data=st.data())
@pytest.mark.parametrize("pattern", BYTES_PATTERNS)
def test_returns_false_with_bytes_pattern_and_str_value(
    data: st.DataObject, pattern: bytes
) -> None:
    value = data.draw(st_from_bytes_pattern(pattern))

    assert (result := matches_pattern(pattern))

    constraint = unwrap_success(result)
    assert constraint != value.decode()
