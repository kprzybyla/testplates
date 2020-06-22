from typing import Literal, Final

from hypothesis import given, strategies as st

from testplates.boundaries.utils import get_minimum, get_maximum

MINIMUM_EXTREMUM: Final[Literal["minimum"]] = "minimum"
MAXIMUM_EXTREMUM: Final[Literal["maximum"]] = "maximum"


def test_get_boundaries_success_inclusive() -> None:
    pass


def test_get_boundaries_success_exclusive() -> None:
    pass


def test_get_boundaries_success_unlimited() -> None:
    pass


def test_get_boundaries_failure_due_to_missing_boundary() -> None:
    pass


def test_get_boundaries_failure_due_to_mutually_exclusive_boundaries() -> None:
    pass


@given(inclusive=st.integers(), exclusive=st.integers())
def test_get_minimum(mocker, inclusive, exclusive) -> None:
    minimum = object()

    get_boundary = mocker.patch("testplates.boundaries.utils.get_boundary")
    get_boundary.return_value = minimum

    assert get_minimum(inclusive=inclusive, exclusive=exclusive) is minimum
    assert get_boundary.mock_calls == [
        mocker.call(MINIMUM_EXTREMUM, inclusive=inclusive, exclusive=exclusive),
    ]


@given(inclusive=st.integers(), exclusive=st.integers())
def test_get_maximum(mocker, inclusive, exclusive) -> None:
    maximum = object()

    get_boundary = mocker.patch("testplates.boundaries.utils.get_boundary")
    get_boundary.return_value = maximum

    assert get_maximum(inclusive=inclusive, exclusive=exclusive) is maximum
    assert get_boundary.mock_calls == [
        mocker.call(MAXIMUM_EXTREMUM, inclusive=inclusive, exclusive=exclusive),
    ]
