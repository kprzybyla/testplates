from typing import Any

from resultful import unwrap_success
from hypothesis import given

from testplates import passthrough_validator

from tests.strategies import st_anything_comparable


def test_repr() -> None:
    fmt = "testplates.passthrough_validator()"
    validator = unwrap_success(passthrough_validator())
    assert repr(validator) == fmt


@given(data=st_anything_comparable())
def test_success(data: Any) -> None:
    assert (validator_result := passthrough_validator())

    validator = unwrap_success(validator_result)
    assert (validation_result := validator(data))

    outcome = unwrap_success(validation_result)
    assert outcome is None
