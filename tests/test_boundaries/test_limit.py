from typing import Final

from hypothesis import given
from hypothesis import strategies as st

from testplates.boundaries import Limit, Extremum

from tests.conftest import Draw

EXCLUSIVE_NAME: Final[str] = "exclusive"

INCLUSIVE_ALIGNMENT: Final[int] = 0
EXCLUSIVE_ALIGNMENT: Final[int] = 1


@st.composite
def st_extremum(draw: Draw[Extremum]) -> Extremum:
    return draw(st.one_of(st.just("minimum"), st.just("maximum")))


@given(name=st_extremum(), value=st.integers())
def test_inclusive_repr(name: Extremum, value: int) -> None:
    fmt = "{name}={value}"

    inclusive = Limit(name, value, is_inclusive=True)

    assert repr(inclusive) == fmt.format(name=name, value=value)


@given(name=st_extremum(), value=st.integers())
def test_inclusive_properties(name: Extremum, value: int) -> None:
    inclusive = Limit(name, value, is_inclusive=True)

    assert inclusive.name == name
    assert inclusive.value == value
    assert inclusive.alignment == INCLUSIVE_ALIGNMENT
    assert inclusive.is_inclusive


@given(name=st_extremum(), value=st.integers())
def test_exclusive_repr(name: Extremum, value: int) -> None:
    fmt = "{type}_{name}={value}"

    inclusive = Limit(name, value, is_inclusive=False)

    assert repr(inclusive) == fmt.format(name=name, value=value, type=EXCLUSIVE_NAME)


@given(name=st_extremum(), value=st.integers())
def test_exclusive_properties(name: Extremum, value: int) -> None:
    exclusive = Limit(name, value, is_inclusive=False)

    assert exclusive.name == name
    assert exclusive.value == value
    assert exclusive.alignment == EXCLUSIVE_ALIGNMENT
    assert not exclusive.is_inclusive
