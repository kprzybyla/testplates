import sys

from typing import Final

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import has_length_between

from tests.conftest import Draw

MINIMUM_LENGTH: Final[int] = 0
MAXIMUM_LENGTH: Final[int] = sys.maxsize


@st.composite
def st_length(
    draw: Draw[int], min_value: int = MINIMUM_LENGTH, max_value: int = MAXIMUM_LENGTH
) -> int:
    return draw(st.integers(min_value=min_value, max_value=max_value))


@st.composite
def st_minimum(draw: Draw[int], length: int) -> int:
    return draw(st.integers(min_value=MINIMUM_LENGTH, max_value=length))


@st.composite
def st_maximum(draw: Draw[int], length: int) -> int:
    return draw(st.integers(min_value=length, max_value=MAXIMUM_LENGTH))


# noinspection PyTypeChecker
@given(data=st.data(), length=st_length())
def test_repr_with_minimum_and_maximum(data: st.DataObject, length: int) -> None:
    fmt = "testplates.has_length_between(minimum={minimum}, maximum={maximum})"

    minimum = data.draw(st_minimum(length))
    maximum = data.draw(st_maximum(length))

    assume(minimum != maximum)

    constraint = has_length_between(minimum=minimum, maximum=maximum)

    assert repr(constraint) == fmt.format(minimum=minimum, maximum=maximum)
