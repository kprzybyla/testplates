__all__ = ["is_permutation_of"]

from typing import Any, TypeVar, Generic, Iterable

from testplates import __module__
from testplates.abc import Constraint

_T = TypeVar("_T", covariant=True)


class IsPermutationOf(Generic[_T], Constraint):

    __slots__ = ("_values",)

    def __init__(self, *values: _T) -> None:
        self._values = values

    def __repr__(self) -> str:
        return f"{__module__}.{type(self).__name__}[{self._values!r}]"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Iterable):
            return False

        values = list(self._values)

        for value in other:
            try:
                found = values.index(value)
            except IndexError:
                return False
            else:
                values.pop(found)

        return len(values) == 0


def is_permutation_of(*values: Any) -> IsPermutationOf[Any]:
    return IsPermutationOf(*values)
