__all__ = ["Contains"]

from typing import Any, TypeVar, Generic, Container, Final

import testplates

from testplates.impl.utils import format_like_tuple

from .exceptions import InsufficientValuesError

_T = TypeVar("_T")


class Contains(Generic[_T]):

    __slots__ = ("values",)

    def __init__(self, *values: _T) -> None:
        self.values = values

    def __repr__(self) -> str:
        return f"{testplates.__name__}.contains({format_like_tuple(self.values)})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Container):
            return False

        for value in self.values:
            if value not in other:
                return False

        return True
