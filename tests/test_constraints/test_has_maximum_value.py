from typing import Any, Optional, Literal, Final

from resultful import (
    unwrap_success,
    unwrap_failure,
)

from hypothesis import (
    assume,
    given,
    strategies as st,
)

from testplates import (
    has_maximum_value,
    MissingBoundaryError,
    MutuallyExclusiveBoundariesError,
)

from tests.strategies import Draw

MAXIMUM_EXTREMUM: Final[Literal["maximum"]] = "maximum"

EXCLUSIVE_ALIGNMENT: Final[int] = 1


class NotComparable:

    __slots__ = ()

    def __gt__(self, other: Any) -> bool:
        return NotImplemented

    def __lt__(self, other: Any) -> bool:
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        return NotImplemented


@st.composite
def st_value(
    draw: Draw[int],
    min_value: Optional[int] = None,
    max_value: Optional[int] = None,
) -> int:
    return draw(st.integers(min_value=min_value, max_value=max_value))


@st.composite
def st_inclusive_maximum(draw: Draw[int], value: int) -> int:
    return draw(st.integers(min_value=value))


@st.composite
def st_exclusive_maximum(draw: Draw[int], value: int) -> int:
    maximum = draw(st_inclusive_maximum(value))
    assume(value != maximum)

    return maximum


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_repr_with_inclusive_maximum(
    data: st.DataObject,
    value: int,
) -> None:
    fmt = "testplates.has_maximum_value(maximum={maximum})"

    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    assert (result := has_maximum_value(maximum=inclusive_maximum))

    constraint = unwrap_success(result)
    assert repr(constraint) == fmt.format(maximum=inclusive_maximum)


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_repr_with_exclusive_maximum(
    data: st.DataObject,
    value: int,
) -> None:
    fmt = "testplates.has_maximum_value(exclusive_maximum={maximum})"

    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    assert (result := has_maximum_value(exclusive_maximum=exclusive_maximum))

    constraint = unwrap_success(result)
    assert repr(constraint) == fmt.format(maximum=exclusive_maximum)


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_success_with_exclusive_minimum_and_inclusive_maximum(
    data: st.DataObject,
    value: int,
) -> None:
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    assert (result := has_maximum_value(maximum=inclusive_maximum))

    constraint = unwrap_success(result)
    assert constraint == value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_success_with_exclusive_maximum(
    data: st.DataObject,
    value: int,
) -> None:
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    assert (result := has_maximum_value(exclusive_maximum=exclusive_maximum))

    constraint = unwrap_success(result)
    assert constraint == value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_above_exclusive_minimum_and_inclusive_maximum(
    data: st.DataObject,
    value: int,
) -> None:
    inclusive_maximum = data.draw(st_value(max_value=value))

    assume(inclusive_maximum != value)

    assert (result := has_maximum_value(maximum=inclusive_maximum))

    constraint = unwrap_success(result)
    assert constraint != value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_above_exclusive_minimum_and_exclusive_maximum(
    data: st.DataObject,
    value: int,
) -> None:
    exclusive_maximum = data.draw(st_value(max_value=value))

    assert (result := has_maximum_value(exclusive_maximum=exclusive_maximum))

    constraint = unwrap_success(result)
    assert constraint != value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_not_comparable_with_inclusive_boundary(
    data: st.DataObject,
    value: int,
) -> None:
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    assert (result := has_maximum_value(maximum=inclusive_maximum))

    constraint = unwrap_success(result)
    assert constraint != NotComparable()


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_not_comparable_with_exclusive_boundary(
    data: st.DataObject,
    value: int,
) -> None:
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    assert (result := has_maximum_value(exclusive_maximum=exclusive_maximum))

    constraint = unwrap_success(result)
    assert constraint != NotComparable()


def test_failure_when_boundaries_are_missing() -> None:
    assert not (result := has_maximum_value())

    error = unwrap_failure(result)
    assert isinstance(error, MissingBoundaryError)


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_mutually_exclusive_boundaries_are_set(
    data: st.DataObject,
    value: int,
) -> None:
    inclusive_maximum = data.draw(st_inclusive_maximum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    assert not (
        result := has_maximum_value(
            maximum=inclusive_maximum,
            exclusive_maximum=exclusive_maximum,
        )
    )

    error = unwrap_failure(result)
    assert isinstance(error, MutuallyExclusiveBoundariesError)
    assert error.name == MAXIMUM_EXTREMUM
