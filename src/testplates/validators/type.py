__all__ = ["type_validator", "validate_any"]

from typing import Any, Tuple, Union, Callable, Optional

from .exceptions import InvalidTypeError


def type_validator(
    *, allowed_types: Union[type, Tuple[type, ...]]
) -> Callable[[Any], Optional[Exception]]:
    def validate(data: Any) -> Optional[Exception]:
        if not isinstance(data, allowed_types):
            return InvalidTypeError(data, allowed_types)

        return None

    return validate


# noinspection PyUnusedLocal
def validate_any(data: Any) -> Optional[Exception]:
    return None
