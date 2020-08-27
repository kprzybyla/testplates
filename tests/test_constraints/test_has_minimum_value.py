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
    has_minimum_value,
    MissingBoundaryError,
    MutuallyExclusiveBoundariesError,
)

from tests.strategies import Draw

MINIMUM_EXTREMUM: Final[Literal["minimum"]] = "minimum"

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
def st_inclusive_minimum(draw: Draw[int], value: int) -> int:
    return draw(st.integers(max_value=value))


@st.composite
def st_exclusive_minimum(draw: Draw[int], value: int) -> int:
    minimum = draw(st_inclusive_minimum(value))
    assume(value != minimum)

    return minimum


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_repr_with_inclusive_minimum(data: st.DataObject, value: int) -> None:
    fmt = "testplates.has_minimum_value(minimum={minimum})"

    inclusive_minimum = data.draw(st_inclusive_minimum(value))

    assert (result := has_minimum_value(minimum=inclusive_minimum))

    constraint = unwrap_success(result)
    assert repr(constraint) == fmt.format(minimum=inclusive_minimum)


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_repr_with_exclusive_minimum(data: st.DataObject, value: int) -> None:
    fmt = "testplates.has_minimum_value(exclusive_minimum={minimum})"

    exclusive_minimum = data.draw(st_exclusive_minimum(value))

    assert (result := has_minimum_value(exclusive_minimum=exclusive_minimum))

    constraint = unwrap_success(result)
    assert repr(constraint) == fmt.format(minimum=exclusive_minimum)


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_success_with_inclusive_minimum(data: st.DataObject, value: int) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))

    assert (result := has_minimum_value(minimum=inclusive_minimum))

    constraint = unwrap_success(result)
    assert constraint == value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_success_with_exclusive_minimum(data: st.DataObject, value: int) -> None:
    exclusive_minimum = data.draw(st_exclusive_minimum(value))

    assert (result := has_minimum_value(exclusive_minimum=exclusive_minimum))

    constraint = unwrap_success(result)
    assert constraint == value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_below_inclusive_minimum(data: st.DataObject, value: int) -> None:
    inclusive_minimum = data.draw(st_value(min_value=value))

    assume(inclusive_minimum != value)

    assert (result := has_minimum_value(minimum=inclusive_minimum))

    constraint = unwrap_success(result)
    assert constraint != value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_below_exclusive_minimum(data: st.DataObject, value: int) -> None:
    exclusive_minimum = data.draw(st_value(min_value=value))

    assert (result := has_minimum_value(exclusive_minimum=exclusive_minimum))

    constraint = unwrap_success(result)
    assert constraint != value


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_not_comparable_with_inclusive_boundary(
    data: st.DataObject,
    value: int,
) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))

    assert (result := has_minimum_value(minimum=inclusive_minimum))

    constraint = unwrap_success(result)
    assert constraint != NotComparable()


# noinspection PyTypeChecker
@given(data=st.data(), value=st_value())
def test_failure_when_value_is_not_comparable_with_exclusive_boundary(
    data: st.DataObject,
    value: int,
) -> None:
    exclusive_minimum = data.draw(st_exclusive_minimum(value))

    assert (result := has_minimum_value(exclusive_minimum=exclusive_minimum))

    constraint = unwrap_success(result)
    assert constraint != NotComparable()


# noinspection PyArgumentList
def test_failure_when_boundaries_are_missing() -> None:
    assert not (result := has_minimum_value())

    error = unwrap_failure(result)
    assert isinstance(error, MissingBoundaryError)


# noinspection PyTypeChecker
# noinspection PyArgumentList
@given(data=st.data(), value=st_value())
def test_failure_when_mutually_exclusive_boundaries_are_set(
    data: st.DataObject,
    value: int,
) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    exclusive_minimum = data.draw(st_exclusive_minimum(value))

    assert not (
        result := has_minimum_value(
            minimum=inclusive_minimum,
            exclusive_minimum=exclusive_minimum,
        )
    )

    error = unwrap_failure(result)
    assert isinstance(error, MutuallyExclusiveBoundariesError)
    assert error.name == MINIMUM_EXTREMUM
