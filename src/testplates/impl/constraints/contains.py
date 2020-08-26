__all__ = ("Contains",)

from typing import (
    Any,
    TypeVar,
    Generic,
    Container,
)

import testplates

from testplates.impl.utils import format_like_tuple

_T = TypeVar("_T")


class Contains(Generic[_T]):

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
        if not isinstance(other, Container):
            return False

        for value in self.values:
            if value not in other:
                return False

        return True
