from typing import Any

from hypothesis import given

from testplates import Success
from testplates.validators import passthrough_validator

from tests.conftest import st_anything_comparable


def test_repr() -> None:
    fmt = "testplates.passthrough_validator()"

    assert repr(passthrough_validator) == fmt


@given(data=st_anything_comparable())
def test_success(data: Any) -> None:
    validation_result = passthrough_validator(data)
    value = Success.from_result(validation_result).value

    assert value is None
