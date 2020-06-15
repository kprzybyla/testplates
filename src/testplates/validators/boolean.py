__all__ = ["boolean_validator"]

from typing import Optional, Final

from .type import type_validator
from .utils import Result, Validator

validate_boolean_type: Final = type_validator(allowed_types=bool)


def boolean_validator() -> Result[Validator[bool]]:
    def validate(data: bool) -> Optional[Exception]:
        return validate_boolean_type(data)

    return validate
