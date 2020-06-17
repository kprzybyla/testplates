from typing import TypeVar, Final

from hypothesis import given, strategies as st

from testplates.boundaries import Limit

from tests.conftest import st_anything_comparable

_T = TypeVar("_T", int, float)

INCLUSIVE_NAME: Final[str] = "inclusive"
EXCLUSIVE_NAME: Final[str] = "exclusive"

INCLUSIVE_ALIGNMENT: Final[int] = 0
EXCLUSIVE_ALIGNMENT: Final[int] = 1


@given(name=st.text(), value=st_anything_comparable())
def test_inclusive_repr(name: str, value: _T) -> None:
    fmt = "{name}={value}"

    inclusive = Limit(name, value, is_inclusive=True)

    assert repr(inclusive) == fmt.format(name=name, value=value)


@given(name=st.text(), value=st_anything_comparable())
def test_inclusive_properties(name: str, value: _T) -> None:
    inclusive = Limit(name, value, is_inclusive=True)

    assert inclusive.name == name
    assert inclusive.value == value
    assert inclusive.alignment == INCLUSIVE_ALIGNMENT
    assert inclusive.is_inclusive


@given(name=st.text(), value=st_anything_comparable())
def test_exclusive_repr(name: str, value: _T) -> None:
    fmt = "{type}_{name}={value}"

    inclusive = Limit(name, value, is_inclusive=False)

    assert repr(inclusive) == fmt.format(name=name, value=value, type=EXCLUSIVE_NAME)


@given(name=st.text(), value=st_anything_comparable())
def test_exclusive_properties(name: str, value: _T) -> None:
    exclusive = Limit(name, value, is_inclusive=False)

    assert exclusive.name == name
    assert exclusive.value == value
    assert exclusive.alignment == EXCLUSIVE_ALIGNMENT
    assert not exclusive.is_inclusive
