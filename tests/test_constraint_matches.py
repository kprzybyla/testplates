import pytest

from hypothesis import given
from hypothesis import strategies as st

from testplates import matches


@given(data=st.data())
@pytest.mark.parametrize("pattern", [r"\d+"])
def test_matches_string(data: st.DataObject, pattern: str) -> None:
    value = data.draw(st.from_regex(pattern, fullmatch=True))

    assert matches(pattern) == value


@given(data=st.data())
@pytest.mark.parametrize("pattern", [r"\d+"])
def test_matches_string_always_returns_false_on_str_value(
    data: st.DataObject, pattern: str
) -> None:
    value = data.draw(st.from_regex(pattern, fullmatch=True))

    assert matches(pattern) != value.encode()


@given(data=st.data())
@pytest.mark.parametrize("pattern", [rb"\d+"])
def test_matches_bytes(data: st.DataObject, pattern: bytes) -> None:
    value = data.draw(st.from_regex(pattern, fullmatch=True))

    assert matches(pattern) == value


@given(data=st.data())
@pytest.mark.parametrize("pattern", [rb"\d+"])
def test_matches_bytes_always_returns_false_on_str_value(
    data: st.DataObject, pattern: bytes
) -> None:
    value = data.draw(st.from_regex(pattern, fullmatch=True))

    assert matches(pattern) != value.decode()
