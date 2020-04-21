__all__ = ["Boolean"]

from .base_validator import BaseValidator
from .exceptions import InvalidTypeError


class Boolean(BaseValidator[bool]):

    __slots__ = ()

    def validate(self, data: bool) -> None:
        if not isinstance(data, bool):
            raise InvalidTypeError(data, bool)
