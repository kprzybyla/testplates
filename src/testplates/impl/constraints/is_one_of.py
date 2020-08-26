__all__ = ("IsOneOf",)

from typing import (
    Any,
    TypeVar,
    Generic,
)

import testplates

from testplates.impl.utils import format_like_tuple

_T = TypeVar("_T")


class IsOneOf(Generic[_T]):

    __slots__ = (
        "name",
        "values",
    )

    def __init__(self, name: str, *values: _T) -> None:
        self.name = name
        self.values = values

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{self.name}({format_like_tuple(self.values)})"

    def __eq__(self, other: Any) -> bool:
        return other in self.values
