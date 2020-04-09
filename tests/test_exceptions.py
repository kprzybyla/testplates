from typing import Any, Generic, Tuple, Union
from collections import Counter

from testplates.exceptions import (
    TestplatesError,
    TestplatesValueError,
    DanglingDescriptorError,
    MissingValueError,
    InvalidLengthError,
    UnexpectedValueError,
    ProhibitedValueError,
    MissingBoundaryError,
    MutuallyExclusiveBoundariesError,
    OverlappingBoundariesError,
    SingleMatchBoundariesError,
    InsufficientValuesError,
    InternalError,
    MissingValueInternalError,
    UnreachableCodeExecutionInternalError,
)

from hypothesis import given
from hypothesis import strategies as st


def is_direct_instance(object: Any, bases: Union[Any, Tuple[Any, ...]]) -> bool:
    if not isinstance(bases, tuple):
        bases = (bases,)

    return Counter(type(object).__bases__) == Counter(bases)


@given(message=st.text())
def test_testplates_error(message: str) -> None:
    error = TestplatesError(message)

    assert is_direct_instance(error, Exception)

    assert message in error.message


@given(message=st.text())
def test_testplates_value_error(message: str) -> None:
    error = TestplatesValueError(message)

    assert is_direct_instance(error, (TestplatesError, ValueError))

    assert message in error.message


@given(descriptor=st.text())
def test_dangling_descriptor_error(descriptor: str) -> None:
    error = DanglingDescriptorError(descriptor)  # type: ignore

    assert is_direct_instance(error, TestplatesError)

    assert descriptor == error.descriptor  # type: ignore
    assert repr(descriptor) in error.message


@given(field=st.text())
def test_missing_value_error(field: str) -> None:
    error = MissingValueError(field)  # type: ignore

    assert is_direct_instance(error, TestplatesValueError)

    assert field == error.field  # type: ignore
    assert repr(field) in error.message


@given(boundary=st.integers())
def test_invalid_length_error(boundary: int) -> None:
    error = InvalidLengthError(boundary)  # type: ignore

    assert is_direct_instance(error, TestplatesValueError)

    assert boundary == error.boundary  # type: ignore
    assert repr(boundary) in error.message


@given(key=st.text(), value=st.integers())
def test_unexpected_value_error(key: str, value: int) -> None:
    error = UnexpectedValueError(key, value)

    assert is_direct_instance(error, TestplatesValueError)

    assert key == error.key
    assert value == error.value

    assert repr(key) in error.message
    assert repr(value) in error.message


@given(field=st.text(), value=st.integers())
def test_prohibited_value_error(field: str, value: int) -> None:
    error = ProhibitedValueError(field, value)  # type: ignore

    assert is_direct_instance(error, TestplatesValueError)

    assert field == error.field  # type: ignore
    assert value == error.value

    assert repr(field) in error.message
    assert repr(value) in error.message


@given(name=st.text())
def test_missing_boundary_error(name: str) -> None:
    error = MissingBoundaryError(name)

    assert is_direct_instance(error, TestplatesValueError)

    assert name == error.name
    assert repr(name) in error.message


@given(name=st.text())
def test_mutually_exclusive_boundaries_error(name: str) -> None:
    error = MutuallyExclusiveBoundariesError(name)

    assert is_direct_instance(error, TestplatesValueError)

    assert name == error.name
    assert repr(name) in error.message


@given(minimum=st.integers(), maximum=st.integers())
def test_overlapping_boundaries_error(minimum: int, maximum: int) -> None:
    error = OverlappingBoundariesError(minimum, maximum)  # type: ignore

    assert is_direct_instance(error, (TestplatesValueError, Generic))

    assert minimum == error.minimum  # type: ignore
    assert maximum == error.maximum  # type: ignore

    assert repr(minimum) in error.message
    assert repr(maximum) in error.message


@given(minimum=st.integers(), maximum=st.integers())
def test_single_match_boundaries_error(minimum: int, maximum: int) -> None:
    error = SingleMatchBoundariesError(minimum, maximum)  # type: ignore

    assert is_direct_instance(error, (TestplatesValueError, Generic))

    assert minimum == error.minimum  # type: ignore
    assert maximum == error.maximum  # type: ignore

    assert repr(minimum) in error.message
    assert repr(maximum) in error.message


@given(required=st.integers())
def test_insufficient_values_error(required: int) -> None:
    error = InsufficientValuesError(required)

    assert is_direct_instance(error, TestplatesValueError)

    assert required == error.required
    assert repr(required) in error.message


@given(message=st.text())
def test_internal_error(message: str) -> None:
    error = InternalError(message)

    assert is_direct_instance(error, TestplatesError)

    assert message in error.message


@given(field=st.text())
def test_missing_value_internal_error(field: str) -> None:
    error = MissingValueInternalError(field)  # type: ignore

    assert is_direct_instance(error, InternalError)

    assert field == error.field  # type: ignore
    assert repr(field) in error.message


def test_unreachable_code_internal_error() -> None:
    error = UnreachableCodeExecutionInternalError()

    assert is_direct_instance(error, InternalError)