__all__ = ["contains"]

from typing import Any, TypeVar, Generic, Container

from testplates import __module__
from testplates.exceptions import NotEnoughValuesError

from .constraint import Constraint

_T = TypeVar("_T", covariant=True)


class Contains(Generic[_T], Constraint):

    __slots__ = ("_values",)

    def __init__(self, *values: _T) -> None:
        if len(values) == 0:
            raise NotEnoughValuesError()

        self._values = values

    def __repr__(self) -> str:
        return f"{__module__}.{type(self).__name__}{list(self._values)!r}"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Container):
            return False

        for value in self._values:
            if value not in other:
                return False

        return True


def contains(*values: Any) -> Contains[Any]:
    return Contains(*values)
