__all__ = ["boolean_validator"]

from typing import Callable, Optional, Final

from .type import type_validator

validate_boolean_type: Final = type_validator(allowed_types=bool)


def boolean_validator() -> Callable[[bool], Optional[Exception]]:
    def validate(data: bool) -> Optional[Exception]:
        return validate_boolean_type(data)

    return validate
