from typing import Any

import pytest

from hypothesis import given
from testplates import Success, Failure

from tests.conftest import st_anything_comparable


@given(value=st_anything_comparable())
def test_repr(value: Any) -> None:
    fmt = "testplates.Success({value})"

    success = Success(value)

    assert repr(success) == fmt.format(value=value)


@given(value=st_anything_comparable())
def test_from_result(value: Any) -> None:
    success = Success.from_result(Success(value))

    assert success.is_success
    assert success.value == value


@given(error=st_anything_comparable())
def test_from_result_failure(error: Any) -> None:
    with pytest.raises(AssertionError):
        Success.from_result(Failure(error))


@given(value=st_anything_comparable())
def test_value(value: Any) -> None:
    success = Success(value)

    assert success.value == value


# noinspection PyStatementEffect
@given(value=st_anything_comparable())
def test_error(value: Any) -> None:
    success = Success(value)

    with pytest.raises(NotImplementedError):
        success.error
