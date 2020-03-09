__all__ = ["is_permutation_of"]

from typing import Any, TypeVar, Generic, List, Iterable

from testplates import __module__
from testplates.abc import Constraint
from testplates.exceptions import TooLittleValuesError

_T = TypeVar("_T", covariant=True)


class IsPermutationOf(Generic[_T], Constraint):

    __slots__ = ("_values",)

    def __init__(self, *values: _T) -> None:
        if len(values) < 2:
            raise TooLittleValuesError()

        self._values = values

    def __repr__(self) -> str:
        return f"{__module__}.{type(self).__name__}[{self._values!r}]"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Iterable):
            return False

        if len(other) != len(self._values):
            return False

        values = list(self._values)

        for value in other:
            try:
                index = values.index(value)
            except ValueError:
                return False
            else:
                values.pop(index)

        return True


def is_permutation_of(*values: Any) -> IsPermutationOf[Any]:
    return IsPermutationOf(*values)
