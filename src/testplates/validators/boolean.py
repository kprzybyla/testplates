__all__ = ["boolean_validator"]

from typing import Final

from testplates.result import Result, Success

from .type import type_validator
from .utils import Validator

validate_boolean_type: Final = type_validator(allowed_types=bool).value


def boolean_validator() -> Result[Validator[bool]]:
    def validate(data: bool) -> Result[None]:
        return validate_boolean_type(data)

    return Success(validate)
