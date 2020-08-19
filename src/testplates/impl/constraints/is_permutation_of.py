__all__ = ["IsPermutationOf"]

from typing import Any, TypeVar, Generic, List, Collection, Final

import testplates

from .exceptions import InsufficientValuesError

_T = TypeVar("_T")


class IsPermutationOf(Generic[_T]):

    __slots__ = ("values",)

    def __init__(self, values: List[_T], /) -> None:
        self.values = values

    def __repr__(self) -> str:
        return f"{testplates.__name__}.is_permutation_of({self.values!r})"

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
