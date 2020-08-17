__all__ = ["TypeValidator"]

from typing import Any

from resultful import success, failure, Result

import testplates

from testplates.impl.base import TestplatesError
from testplates.impl.utils import format_like_tuple

from .exceptions import InvalidTypeError


class TypeValidator:

    __slots__ = ("allowed_types",)

    def __init__(self, *allowed_types: type) -> None:
        self.allowed_types = allowed_types

    def __repr__(self) -> str:
        allowed_types = format_like_tuple(self.allowed_types)

        return f"{testplates.__name__}.{type(self).__name__}({allowed_types})"

    def __call__(self, data: Any, /) -> Result[None, TestplatesError]:
        allowed_types = self.allowed_types

        if not isinstance(data, allowed_types):
            return failure(InvalidTypeError(data, allowed_types))

        return success(None)
