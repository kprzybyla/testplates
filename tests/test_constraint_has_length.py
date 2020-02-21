import sys

from dataclasses import dataclass

import pytest

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import has_length, MutuallyExclusiveBoundaryValueError

from .conftest import Draw


@dataclass
class Sized:

    length: int

    def __len__(self) -> int:
        return self.length


class NotSized:

    __len__ = None


@st.composite
def st_length(draw: Draw) -> int:
    return draw(st.integers(min_value=0, max_value=sys.maxsize))


@st.composite
def st_inclusive_minimum(draw: Draw, length: int) -> int:
    return draw(st.integers(min_value=0, max_value=length))


@st.composite
def st_inclusive_maximum(draw: Draw, length: int) -> int:
    return draw(st.integers(min_value=length, max_value=sys.maxsize))


@st.composite
def st_exclusive_minimum(draw: Draw, length: int) -> int:
    minimum = draw(st_inclusive_minimum(length))
    assume(minimum < length)

    return minimum


@st.composite
def st_exclusive_maximum(draw: Draw, length: int) -> int:
    maximum = draw(st_inclusive_maximum(length))
    assume(length < maximum)

    return maximum


@st.composite
def st_inverse_inclusive_minimum(draw: Draw, length: int) -> int:
    return draw(st_exclusive_maximum(length))


@st.composite
def st_inverse_inclusive_maximum(draw: Draw, length: int) -> int:
    return draw(st_exclusive_minimum(length))


@st.composite
def st_inverse_exclusive_minimum(draw: Draw, length: int) -> int:
    return draw(st_inclusive_maximum(length))


@st.composite
def st_inverse_exclusive_maximum(draw: Draw, length: int) -> int:
    return draw(st_inclusive_minimum(length))


@given(length=st_length())
def test_has_length_returns_true(length: int) -> None:
    assert has_length(length) == Sized(length)


@given(data=st.data(), length=st_length())
def test_has_length_returns_true_with_exclusive_minimum(data: st.DataObject, length: int) -> None:
    template = has_length(exclusive_minimum=data.draw(st_exclusive_minimum(length)))

    assert template == Sized(length)


@given(data=st.data(), length=st_length())
def test_has_length_returns_true_with_exclusive_maximum(data: st.DataObject, length: int) -> None:
    template = has_length(exclusive_maximum=data.draw(st_exclusive_maximum(length)))

    assert template == Sized(length)


@given(data=st.data(), length=st_length())
def test_has_length_returns_true_with_exclusive_minimum_and_maximum(
    data: st.DataObject, length: int
) -> None:
    template = has_length(
        exclusive_minimum=data.draw(st_exclusive_minimum(length)),
        exclusive_maximum=data.draw(st_exclusive_maximum(length)),
    )

    assert template == Sized(length)


@given(data=st.data(), length=st_length())
def test_has_length_returns_true_with_inclusive_minimum(data: st.DataObject, length: int) -> None:
    template = has_length(inclusive_minimum=data.draw(st_inclusive_minimum(length)))

    assert template == Sized(length)


@given(data=st.data(), length=st_length())
def test_has_length_returns_true_with_inclusive_maximum(data: st.DataObject, length: int) -> None:
    template = has_length(inclusive_maximum=data.draw(st_inclusive_maximum(length)))

    assert template == Sized(length)


@given(data=st.data(), length=st_length())
def test_has_length_returns_true_with_inclusive_minimum_and_maximum(
    data: st.DataObject, length: int
) -> None:
    template = has_length(
        inclusive_minimum=data.draw(st_inclusive_minimum(length)),
        inclusive_maximum=data.draw(st_inclusive_maximum(length)),
    )

    assert template == Sized(length)


@given(data=st.data(), length=st_length())
def test_has_length_returns_true_with_exclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, length: int
) -> None:
    template = has_length(
        inclusive_minimum=data.draw(st_exclusive_minimum(length)),
        inclusive_maximum=data.draw(st_inclusive_maximum(length)),
    )

    assert template == Sized(length)


@given(data=st.data(), length=st_length())
def test_has_length_returns_true_with_inclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, length: int
) -> None:
    template = has_length(
        inclusive_minimum=data.draw(st_inclusive_minimum(length)),
        inclusive_maximum=data.draw(st_exclusive_maximum(length)),
    )

    assert template == Sized(length)


@given(length=st_length(), other=st_length())
def test_has_length_returns_false(length: int, other: int) -> None:
    assume(length != other)

    assert has_length(length) != Sized(other)


@given(data=st.data(), length=st_length())
def test_has_length_returns_false_with_exclusive_minimum(data: st.DataObject, length: int) -> None:
    template = has_length(exclusive_minimum=data.draw(st_inverse_exclusive_minimum(length)))

    assert template != Sized(length)


@given(data=st.data(), length=st_length())
def test_has_length_returns_false_with_exclusive_maximum(data: st.DataObject, length: int) -> None:
    template = has_length(exclusive_maximum=data.draw(st_inverse_exclusive_maximum(length)))

    assert template != Sized(length)


@given(data=st.data(), length=st_length())
def test_has_length_returns_false_with_exclusive_minimum_and_maximum(
    data: st.DataObject, length: int
) -> None:
    template = has_length(
        exclusive_minimum=data.draw(st_inverse_exclusive_minimum(length)),
        exclusive_maximum=data.draw(st_inverse_exclusive_maximum(length)),
    )

    assert template != Sized(length)


@given(data=st.data(), length=st_length())
def test_has_length_returns_false_with_inclusive_minimum(data: st.DataObject, length: int) -> None:
    template = has_length(inclusive_minimum=data.draw(st_inverse_inclusive_minimum(length)))

    assert template != Sized(length)


@given(data=st.data(), length=st_length())
def test_has_length_returns_false_with_inclusive_maximum(data: st.DataObject, length: int) -> None:
    template = has_length(inclusive_maximum=data.draw(st_inverse_inclusive_maximum(length)))

    assert template != Sized(length)


@given(data=st.data(), length=st_length())
def test_has_length_returns_false_with_inclusive_minimum_and_maximum(
    data: st.DataObject, length: int
) -> None:
    template = has_length(
        inclusive_minimum=data.draw(st_inverse_inclusive_minimum(length)),
        inclusive_maximum=data.draw(st_inverse_inclusive_maximum(length)),
    )

    assert template != Sized(length)


@given(data=st.data(), length=st_length())
def test_has_length_returns_false_with_exclusive_minimum_and_inclusive_maximum(
    data: st.DataObject, length: int
) -> None:
    template = has_length(
        inclusive_minimum=data.draw(st_inverse_exclusive_minimum(length)),
        inclusive_maximum=data.draw(st_inverse_inclusive_maximum(length)),
    )

    assert template != Sized(length)


@given(data=st.data(), length=st_length())
def test_has_length_returns_false_with_inclusive_minimum_and_exclusive_maximum(
    data: st.DataObject, length: int
) -> None:
    template = has_length(
        inclusive_minimum=data.draw(st_inverse_inclusive_minimum(length)),
        inclusive_maximum=data.draw(st_inverse_exclusive_maximum(length)),
    )

    assert template != Sized(length)


@given(length=st.integers())
def test_has_length_always_returns_false_when_value_is_not_sized(length: int) -> None:
    assert has_length(length) != NotSized()

    assert has_length(exclusive_minimum=length) != NotSized()
    assert has_length(exclusive_maximum=length) != NotSized()

    assert has_length(inclusive_minimum=length) != NotSized()
    assert has_length(inclusive_maximum=length) != NotSized()


@given(length=st_length())
def test_has_length_raises_value_error_on_mutually_exclusive_minimum_boundaries(
    length: int
) -> None:
    with pytest.raises(ValueError):
        has_length(inclusive_minimum=length, exclusive_minimum=length)

    with pytest.raises(MutuallyExclusiveBoundaryValueError):
        has_length(inclusive_minimum=length, exclusive_minimum=length)


@given(length=st_length())
def test_has_length_raises_value_error_on_mutually_exclusive_maximum_boundaries(
    length: int
) -> None:
    with pytest.raises(ValueError):
        has_length(inclusive_maximum=length, exclusive_maximum=length)

    with pytest.raises(MutuallyExclusiveBoundaryValueError):
        has_length(inclusive_maximum=length, exclusive_maximum=length)


def test_has_length_raises_type_error_on_no_parameters() -> None:
    with pytest.raises(TypeError):
        has_length()
