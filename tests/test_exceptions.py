from testplates.exceptions import (
    TestplatesError,
    InternalError,
    MissingValueInternalError,
    UnreachableCodeExecutionInternalError,
)

from hypothesis import given
from hypothesis import strategies as st


@given(message=st.text())
def test_internal_error(message: str) -> None:
    error = InternalError(message)

    assert type(error).__bases__ == (TestplatesError,)
    assert message in error.message


@given(field=st.text())
def test_missing_value_internal_error(field: str) -> None:
    error = MissingValueInternalError(field)  # type: ignore

    assert isinstance(error, InternalError)
    assert repr(field) in error.message


def test_unreachable_code_internal_error() -> None:
    error = UnreachableCodeExecutionInternalError()

    assert isinstance(error, InternalError)
