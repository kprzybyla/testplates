__all__ = ["TypeValidator"]

from typing import Any, Tuple

import testplates

from testplates.impl.base import Result, Success, Failure
from testplates.impl.base import TestplatesError
from testplates.impl.utils import format_like_tuple

from .exceptions import InvalidTypeError


# noinspection PyTypeChecker
class TypeValidator:

    __slots__ = ("allowed_types",)

    def __init__(self, allowed_types: Tuple[type, ...], /) -> None:
        self.allowed_types = allowed_types

    def __repr__(self) -> str:
        allowed_types = format_like_tuple(self.allowed_types)

        return f"{testplates.__name__}.{type(self).__name__}({allowed_types})"

    def __call__(self, data: Any) -> Result[None, TestplatesError]:
        allowed_types = self.allowed_types

        if not isinstance(data, allowed_types):
            return Failure(InvalidTypeError(data, allowed_types))

        return Success(None)
