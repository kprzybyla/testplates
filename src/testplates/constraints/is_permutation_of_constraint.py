__all__ = ["is_permutation_of"]

from typing import Any, TypeVar, Generic, List, Collection, Final

import testplates

from testplates.abc import Constraint
from testplates.exceptions import InsufficientValuesError

_T = TypeVar("_T", covariant=True)

MINIMUM_NUMBER_OF_VALUES: Final[int] = 2


class IsPermutationOf(Generic[_T], Constraint):

    __slots__ = ("_values",)

    def __init__(self, values: List[_T]) -> None:
        if len(values) < MINIMUM_NUMBER_OF_VALUES:
            raise InsufficientValuesError(MINIMUM_NUMBER_OF_VALUES)

        self._values = values

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{type(self).__name__}{self._values!r}"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Collection):
            return False

        if len(other) != len(self._values):
            return False

        values = self._values.copy()

        for value in other:
            try:
                index = values.index(value)
            except ValueError:
                return False
            else:
                values.pop(index)

        return True


def is_permutation_of(values: Any) -> IsPermutationOf[Any]:
    return IsPermutationOf(values)
