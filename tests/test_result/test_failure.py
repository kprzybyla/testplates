from typing import Any

import pytest

from hypothesis import given
from testplates import Success, Failure

from tests.conftest import st_anything_comparable


@given(error=st_anything_comparable())
def test_repr(error: Any) -> None:
    fmt = "testplates.Failure({error})"

    failure = Failure(error)

    assert repr(failure) == fmt.format(error=error)


@given(error=st_anything_comparable())
def test_from_result(error: Any) -> None:
    failure = Failure.from_result(Failure(error))

    assert not failure.is_success
    assert failure.is_failure
    assert failure.error == error


@given(value=st_anything_comparable())
def test_from_result_success(value: Any) -> None:
    with pytest.raises(AssertionError):
        Failure.from_result(Success(value))


@given(error=st_anything_comparable())
def test_error(error: Any) -> None:
    failure = Failure(error)

    assert not failure.is_success
    assert failure.is_failure
    assert failure.error == error
