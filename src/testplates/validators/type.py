__all__ = ["type_validator", "validate_any"]

from typing import Type, TypeVar, Callable, Optional

from .exceptions import InvalidTypeError

_T = TypeVar("_T")


def type_validator(*, allowed_types: Type[_T]) -> Callable[[_T], Optional[Exception]]:
    def validate(data: _T) -> Optional[Exception]:
        if not isinstance(data, allowed_types):
            return InvalidTypeError(data, allowed_types)

    return validate


# noinspection PyUnusedLocal
def validate_any(data: _T) -> Optional[Exception]:
    return None
