from typing import Any

import pytest

from hypothesis import given
from testplates import success, failure, unwrap_success, unwrap_failure

from tests.conftest import st_anything_comparable


@given(value=st_anything_comparable())
def test_success_repr(value: Any) -> None:
    fmt = "testplates.Success({value})"

    success_object = success(value)

    assert repr(success_object) == fmt.format(value=value)


@given(value=st_anything_comparable())
def test_success_get_value_from_success(value: Any) -> None:
    success_value = unwrap_success(success(value))

    assert success_value == value


@given(error=st_anything_comparable())
def test_success_get_value_from_failure(error: Any) -> None:
    with pytest.raises(AssertionError):
        unwrap_success(failure(error))


@given(value=st_anything_comparable())
def test_success_value(value: Any) -> None:
    success_object = success(value)

    assert success_object.is_success
    assert not success_object.is_failure
    assert success_object.value == value


@given(value=st_anything_comparable())
def test_success_value_wrapped_in_success(value: Any) -> None:
    success_object = success(success(value))

    assert success_object.is_success
    assert not success_object.is_failure
    assert success_object.value == value


@given(error=st_anything_comparable())
def test_failure_repr(error: Any) -> None:
    fmt = "testplates.Failure({error})"

    failure_object = failure(error)

    assert repr(failure_object) == fmt.format(error=error)


@given(error=st_anything_comparable())
def test_failure_get_error_from_failure(error: Any) -> None:
    failure_error = unwrap_failure(failure(error))

    assert failure_error == error


@given(error=st_anything_comparable())
def test_failure_get_error_from_success(error: Any) -> None:
    with pytest.raises(AssertionError):
        unwrap_failure(success(error))


@given(error=st_anything_comparable())
def test_failure_error(error: Any) -> None:
    failure_object = failure(error)

    assert not failure_object.is_success
    assert failure_object.is_failure
    assert failure_object.error == error


@given(error=st_anything_comparable())
def test_failure_error_wrapped_in_failure(error: Any) -> None:
    failure_object = failure(failure(error))

    assert not failure_object.is_success
    assert failure_object.is_failure
    assert failure_object.error == error
