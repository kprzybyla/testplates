import re

from typing import Any, AnyStr, List
from typing_extensions import Final

import pytest

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import matches_pattern

from ..conftest import st_anything_except, Draw

ANY_WORD: Final[str] = r"\w+"
ANY_DIGIT: Final[str] = r"\d+"
MAC_ADDRESS: Final[str] = r"([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})"
HEX_COLOR_NUMBER: Final[str] = r"\B#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})\b"

PATTERNS: Final[List[str]] = [ANY_WORD, ANY_DIGIT, MAC_ADDRESS, HEX_COLOR_NUMBER]


@pytest.fixture(params=PATTERNS)
def str_pattern(request):
    return request.param


@pytest.fixture(params=map(str.encode, PATTERNS))
def bytes_pattern(request):
    return request.param


@st.composite
def st_regex(draw: Draw, pattern: AnyStr) -> AnyStr:
    return draw(st.from_regex(pattern, fullmatch=True))


@st.composite
def st_inverse_str_regex(draw: Draw, pattern: str) -> str:
    text = draw(st.text())
    assume(not re.match(pattern, text))

    return text


@st.composite
def st_inverse_bytes_regex(draw: Draw, pattern: bytes) -> bytes:
    binary = draw(st.binary())
    assume(not re.match(pattern, binary))

    return binary


@given(data=st.data())
def test_returns_true_with_str_pattern(data: st.DataObject, str_pattern: str) -> None:
    value = data.draw(st_regex(str_pattern))

    template = matches_pattern(str_pattern)

    assert template == value


@given(data=st.data())
def test_returns_true_with_bytes_pattern(data: st.DataObject, bytes_pattern: bytes) -> None:
    value = data.draw(st_regex(bytes_pattern))

    template = matches_pattern(bytes_pattern)

    assert template == value


@given(data=st.data())
def test_returns_false_with_str_pattern(data: st.DataObject, str_pattern: str) -> None:
    value = data.draw(st_inverse_str_regex(str_pattern))

    template = matches_pattern(str_pattern)

    assert template != value


@given(data=st.data())
def test_returns_false_with_bytes_pattern(data: st.DataObject, bytes_pattern: bytes) -> None:
    value = data.draw(st_inverse_bytes_regex(bytes_pattern))

    template = matches_pattern(bytes_pattern)

    assert template != value


@given(data=st.data())
def test_returns_false_with_str_pattern_and_bytes_value(
    data: st.DataObject, str_pattern: str
) -> None:
    value = data.draw(st_regex(str_pattern))

    template = matches_pattern(str_pattern)

    assert template != value.encode()


@given(data=st.data())
def test_returns_false_with_bytes_pattern_and_str_value(
    data: st.DataObject, bytes_pattern: bytes
) -> None:
    value = data.draw(st_regex(bytes_pattern))

    template = matches_pattern(bytes_pattern)

    assert template != value.decode()


@given(pattern=st_anything_except(str, bytes))
def test_raises_error_on_invalid_pattern_type(pattern: Any) -> None:
    with pytest.raises(TypeError):
        matches_pattern(pattern)
