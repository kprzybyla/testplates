import re

from typing import Any, List
from typing_extensions import Final

import pytest

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import matches_pattern

from tests.conftest import st_anything_except, Draw

ANY_WORD: Final[str] = r"\w+"
ANY_DIGIT: Final[str] = r"\d+"
MAC_ADDRESS: Final[str] = r"([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})"
HEX_COLOR_NUMBER: Final[str] = r"\B#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})\b"

STR_PATTERNS: Final[List[str]] = [ANY_WORD, ANY_DIGIT, MAC_ADDRESS, HEX_COLOR_NUMBER]
BYTES_PATTERNS: Final[List[bytes]] = list(map(str.encode, STR_PATTERNS))

# TODO(kprzybyla): Implement generic st_regex after following issue is resolved:
#                  https://github.com/HypothesisWorks/hypothesis/issues/2365


@st.composite
def st_str_regex(draw: Draw[str], pattern: str) -> str:
    return draw(st.from_regex(pattern, fullmatch=True))


@st.composite
def st_bytes_regex(draw: Draw[bytes], pattern: bytes) -> bytes:
    return draw(st.from_regex(pattern, fullmatch=True))


@st.composite
def st_inverse_str_regex(draw: Draw[str], pattern: str) -> str:
    text = draw(st.text())
    assume(not re.match(pattern, text))

    return text


@st.composite
def st_inverse_bytes_regex(draw: Draw[bytes], pattern: bytes) -> bytes:
    binary = draw(st.binary())
    assume(not re.match(pattern, binary))

    return binary


@given(data=st.data())
@pytest.mark.parametrize("pattern", STR_PATTERNS)
def test_returns_true_with_str_pattern(data: st.DataObject, pattern: str) -> None:
    value = data.draw(st_str_regex(pattern))

    template = matches_pattern(pattern)

    assert template == value


@given(data=st.data())
@pytest.mark.parametrize("pattern", BYTES_PATTERNS)
def test_returns_true_with_bytes_pattern(data: st.DataObject, pattern: bytes) -> None:
    value = data.draw(st_bytes_regex(pattern))

    template = matches_pattern(pattern)

    assert template == value


@given(data=st.data())
@pytest.mark.parametrize("pattern", STR_PATTERNS)
def test_returns_false_with_str_pattern(data: st.DataObject, pattern: str) -> None:
    value = data.draw(st_inverse_str_regex(pattern))

    template = matches_pattern(pattern)

    assert template != value


@given(data=st.data())
@pytest.mark.parametrize("pattern", BYTES_PATTERNS)
def test_returns_false_with_bytes_pattern(data: st.DataObject, pattern: bytes) -> None:
    value = data.draw(st_inverse_bytes_regex(pattern))

    template = matches_pattern(pattern)

    assert template != value


@given(data=st.data())
@pytest.mark.parametrize("pattern", STR_PATTERNS)
def test_returns_false_with_str_pattern_and_bytes_value(data: st.DataObject, pattern: str) -> None:
    value = data.draw(st_str_regex(pattern))

    template = matches_pattern(pattern)

    assert template != value.encode()


@given(data=st.data())
@pytest.mark.parametrize("pattern", BYTES_PATTERNS)
def test_returns_false_with_bytes_pattern_and_str_value(
    data: st.DataObject, pattern: bytes
) -> None:
    value = data.draw(st_bytes_regex(pattern))

    template = matches_pattern(pattern)

    assert template != value.decode()


@given(pattern=st_anything_except(str, bytes))
def test_raises_error_on_invalid_pattern_type(pattern: Any) -> None:
    with pytest.raises(TypeError):
        matches_pattern(pattern)
