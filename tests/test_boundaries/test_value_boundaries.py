from typing import Optional, Final

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates.boundaries import get_value_boundaries
from testplates import (
    MissingBoundaryError,
    MutuallyExclusiveBoundariesError,
    OverlappingBoundariesError,
    SingleMatchBoundariesError,
)

from tests.conftest import Draw

EXCLUSIVE_ALIGNMENT: Final[int] = 1


@st.composite
def st_value(
    draw: Draw[int], min_value: Optional[int] = None, max_value: Optional[int] = None
) -> int:
    return draw(st.integers(min_value=min_value, max_value=max_value))  # type: ignore


@st.composite
def st_inclusive_minimum(draw: Draw[int], value: int) -> int:
    return draw(st.integers(max_value=value))


@st.composite
def st_inclusive_maximum(draw: Draw[int], value: int) -> int:
    return draw(st.integers(min_value=value))


@st.composite
def st_exclusive_minimum(draw: Draw[int], value: int) -> int:
    minimum = draw(st_inclusive_minimum(value))
    assume(value != minimum)

    return minimum


@st.composite
def st_exclusive_maximum(draw: Draw[int], value: int) -> int:
    maximum = draw(st_inclusive_maximum(value))
    assume(value != maximum)

    return maximum


# noinspection PyArgumentList
def test_raises_error_on_missing_boundaries() -> None:
    result = get_value_boundaries()  # type: ignore

    assert result.is_error
    assert isinstance(result.error, TypeError)


# noinspection PyArgumentList,PyTypeChecker
@given(data=st.data(), value=st_value())
def test_raises_error_on_missing_minimum_boundary(data: st.DataObject, value: int) -> None:
    inclusive_maximum = data.draw(st_inclusive_maximum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    result = get_value_boundaries(inclusive_maximum=inclusive_maximum)  # type: ignore

    assert result.is_error
    assert isinstance(result.error, MissingBoundaryError)

    result = get_value_boundaries(exclusive_maximum=exclusive_maximum)  # type: ignore

    assert result.is_error
    assert isinstance(result.error, MissingBoundaryError)


# noinspection PyArgumentList,PyTypeChecker
@given(data=st.data(), value=st_value())
def test_raises_error_on_missing_maximum_boundary(data: st.DataObject, value: int) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    exclusive_minimum = data.draw(st_exclusive_minimum(value))

    result = get_value_boundaries(inclusive_minimum=inclusive_minimum)  # type: ignore

    assert result.is_error
    assert isinstance(result.error, MissingBoundaryError)

    result = get_value_boundaries(exclusive_minimum=exclusive_minimum)  # type: ignore

    assert result.is_error
    assert isinstance(result.error, MissingBoundaryError)


# noinspection PyArgumentList,PyTypeChecker
@given(data=st.data(), value=st_value())
def test_raises_error_on_mutually_exclusive_minimum_boundaries(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    result = get_value_boundaries(
        inclusive_minimum=inclusive_minimum,
        inclusive_maximum=inclusive_maximum,
        exclusive_minimum=exclusive_minimum,
    )  # type: ignore

    assert result.is_error
    assert isinstance(result.error, MutuallyExclusiveBoundariesError)

    result = get_value_boundaries(
        inclusive_minimum=inclusive_minimum,
        exclusive_minimum=exclusive_minimum,
        exclusive_maximum=exclusive_maximum,
    )  # type: ignore

    assert result.is_error
    assert isinstance(result.error, MutuallyExclusiveBoundariesError)


# noinspection PyArgumentList,PyTypeChecker
@given(data=st.data(), value=st_value())
def test_raises_error_on_mutually_exclusive_maximum_boundaries(
    data: st.DataObject, value: int
) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    result = get_value_boundaries(
        inclusive_minimum=inclusive_minimum,
        inclusive_maximum=inclusive_maximum,
        exclusive_maximum=exclusive_maximum,
    )  # type: ignore

    assert result.is_error
    assert isinstance(result.error, MutuallyExclusiveBoundariesError)

    result = get_value_boundaries(
        inclusive_maximum=inclusive_maximum,
        exclusive_minimum=exclusive_minimum,
        exclusive_maximum=exclusive_maximum,
    )  # type: ignore

    assert result.is_error
    assert isinstance(result.error, MutuallyExclusiveBoundariesError)


# noinspection PyArgumentList,PyTypeChecker
@given(data=st.data(), value=st_value())
def test_raises_error_on_mutually_exclusive_boundaries(data: st.DataObject, value: int) -> None:
    inclusive_minimum = data.draw(st_inclusive_minimum(value))
    inclusive_maximum = data.draw(st_inclusive_maximum(value))

    exclusive_minimum = data.draw(st_exclusive_minimum(value))
    exclusive_maximum = data.draw(st_exclusive_maximum(value))

    result = get_value_boundaries(
        inclusive_minimum=inclusive_minimum,
        inclusive_maximum=inclusive_maximum,
        exclusive_minimum=exclusive_minimum,
        exclusive_maximum=exclusive_maximum,
    )  # type: ignore

    assert result.is_error
    assert isinstance(result.error, MutuallyExclusiveBoundariesError)


# noinspection PyTypeChecker
@given(data=st.data())
def test_raises_error_on_inclusive_minimum_and_inclusive_maximum_overlapping(
    data: st.DataObject,
) -> None:
    inclusive_minimum = data.draw(st_value())
    inclusive_maximum = data.draw(st_value(max_value=inclusive_minimum))

    assume(inclusive_minimum != inclusive_maximum)

    result = get_value_boundaries(
        inclusive_minimum=inclusive_minimum, inclusive_maximum=inclusive_maximum
    )

    assert result.is_error
    assert isinstance(result.error, OverlappingBoundariesError)


# noinspection PyTypeChecker
@given(data=st.data())
def test_raises_error_on_inclusive_minimum_and_exclusive_maximum_overlapping(
    data: st.DataObject,
) -> None:
    inclusive_minimum = data.draw(st_value())
    exclusive_maximum = data.draw(st_value(max_value=inclusive_minimum))

    result = get_value_boundaries(
        inclusive_minimum=inclusive_minimum, exclusive_maximum=exclusive_maximum
    )

    assert result.is_error
    assert isinstance(result.error, OverlappingBoundariesError)


# noinspection PyTypeChecker
@given(data=st.data())
def test_raises_error_on_exclusive_minimum_and_inclusive_maximum_overlapping(
    data: st.DataObject,
) -> None:
    exclusive_minimum = data.draw(st_value())
    inclusive_maximum = data.draw(st_value(max_value=exclusive_minimum))

    result = get_value_boundaries(
        exclusive_minimum=exclusive_minimum, inclusive_maximum=inclusive_maximum
    )

    assert result.is_error
    assert isinstance(result.error, OverlappingBoundariesError)


# noinspection PyTypeChecker
@given(data=st.data())
def test_raises_error_on_exclusive_minimum_and_exclusive_maximum_overlapping(
    data: st.DataObject,
) -> None:
    exclusive_minimum = data.draw(st_value())
    exclusive_maximum = data.draw(st_value(max_value=exclusive_minimum + EXCLUSIVE_ALIGNMENT))

    result = get_value_boundaries(
        exclusive_minimum=exclusive_minimum, exclusive_maximum=exclusive_maximum
    )

    assert result.is_error
    assert isinstance(result.error, OverlappingBoundariesError)


@given(value=st_value())
def test_raises_error_on_single_match_with_inclusive_minimum_and_inclusive_maximum(
    value: int,
) -> None:
    inclusive_minimum = value
    inclusive_maximum = value

    result = get_value_boundaries(
        inclusive_minimum=inclusive_minimum, inclusive_maximum=inclusive_maximum
    )

    assert result.is_error
    assert isinstance(result.error, SingleMatchBoundariesError)


@given(value=st_value())
def test_raises_error_on_single_match_with_inclusive_minimum_and_exclusive_maximum(
    value: int,
) -> None:
    inclusive_minimum = value
    exclusive_maximum = value + EXCLUSIVE_ALIGNMENT

    result = get_value_boundaries(
        inclusive_minimum=inclusive_minimum, exclusive_maximum=exclusive_maximum
    )

    assert result.is_error
    assert isinstance(result.error, SingleMatchBoundariesError)


@given(value=st_value())
def test_raises_error_on_single_match_with_exclusive_minimum_and_inclusive_maximum(
    value: int,
) -> None:
    exclusive_minimum = value - EXCLUSIVE_ALIGNMENT
    inclusive_maximum = value

    result = get_value_boundaries(
        exclusive_minimum=exclusive_minimum, inclusive_maximum=inclusive_maximum
    )

    assert result.is_error
    assert isinstance(result.error, SingleMatchBoundariesError)


@given(value=st_value())
def test_raises_error_on_single_match_with_exclusive_minimum_and_exclusive_maximum(
    value: int,
) -> None:
    exclusive_minimum = value - EXCLUSIVE_ALIGNMENT
    exclusive_maximum = value + EXCLUSIVE_ALIGNMENT

    result = get_value_boundaries(
        exclusive_minimum=exclusive_minimum, exclusive_maximum=exclusive_maximum
    )

    assert result.is_error
    assert isinstance(result.error, SingleMatchBoundariesError)
