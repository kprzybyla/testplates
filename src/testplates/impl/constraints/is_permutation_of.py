__all__ = ("IsPermutationOf",)

import testplates

from typing import (
    Any,
    TypeVar,
    Generic,
    List,
    Collection,
)

_T = TypeVar("_T")


class IsPermutationOf(Generic[_T]):

    __slots__ = (
        "name",
        "values",
    )

    def __init__(self, name: str, values: List[_T], /) -> None:
        self.name = name
        self.values = values

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{self.name}({self.values!r})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Collection):
            return False

        if len(other) != len(self.values):
            return False

        values = self.values.copy()

        for value in other:
            try:
                index = values.index(value)
            except ValueError:
                return False
            else:
                values.pop(index)

        return True
