__all__ = ["Boolean"]

from typing import Type

from .base_validator import BaseValidator


class Boolean(BaseValidator[bool]):

    __slots__ = ()

    @property
    def allowed_types(self) -> Type[bool]:
        return bool
