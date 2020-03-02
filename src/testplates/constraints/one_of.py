__all__ = ["is_one_of"]

from typing import Any, TypeVar, Generic

from testplates import __module__
from testplates.exceptions import NotEnoughValuesError

from .constraint import Constraint

_T = TypeVar("_T", covariant=True)


class IsOneOf(Generic[_T], Constraint):

    __slots__ = ("_values",)

    def __init__(self, *values: _T) -> None:
        if len(values) == 0:
            raise NotEnoughValuesError()

        self._values = values

    def __repr__(self) -> str:
        return f"{__module__}.{type(self).__name__}{list(self._values)!r}"

    def __eq__(self, other: Any) -> bool:
        return other in self._values


def is_one_of(*values: Any) -> IsOneOf[Any]:
    return IsOneOf(*values)
