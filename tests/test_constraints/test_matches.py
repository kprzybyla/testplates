import re

from typing import Any, AnyStr

import pytest

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import matches

from ..conftest import st_anything_except, Draw


@pytest.fixture(params=[r"\d+"])
def str_pattern(request):
    return request.param


@pytest.fixture(params=[rb"\d+"])
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
def test_matches_returns_true_for_str(data: st.DataObject, str_pattern: str) -> None:
    value = data.draw(st_regex(str_pattern))

    assert matches(str_pattern) == value


@given(data=st.data())
def test_matches_returns_true_for_bytes(data: st.DataObject, bytes_pattern: bytes) -> None:
    value = data.draw(st_regex(bytes_pattern))

    assert matches(bytes_pattern) == value


@given(data=st.data())
def test_matches_returns_false_for_str(data: st.DataObject, str_pattern: str) -> None:
    value = data.draw(st_inverse_str_regex(str_pattern))

    assert matches(str_pattern) != value


@given(data=st.data())
def test_matches_returns_false_for_bytes(data: st.DataObject, bytes_pattern: bytes) -> None:
    value = data.draw(st_inverse_bytes_regex(bytes_pattern))

    assert matches(bytes_pattern) != value


@given(data=st.data())
def test_matches_always_returns_false_for_str_pattern_on_bytes_value(
    data: st.DataObject, str_pattern: str
) -> None:
    value = data.draw(st_regex(str_pattern))

    assert matches(str_pattern) != value.encode()


@given(data=st.data())
def test_matches_always_returns_false_for_bytes_pattern_on_str_value(
    data: st.DataObject, bytes_pattern: bytes
) -> None:
    value = data.draw(st_regex(bytes_pattern))

    assert matches(bytes_pattern) != value.decode()


@given(pattern=st_anything_except(str, bytes))
def test_matches_raises_type_error_on_invalid_pattern_type(pattern: Any) -> None:
    with pytest.raises(TypeError):
        matches(pattern)
