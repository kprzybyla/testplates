__all__ = ["contains"]

from typing import Any, TypeVar, Generic, Container

from testplates.exceptions import NotEnoughValuesError

from .constraint import Constraint

_T = TypeVar("_T", covariant=True)


class ContainerTemplate(Generic[_T], Constraint):

    __slots__ = ("_values",)

    def __init__(self, *values: _T) -> None:
        if len(values) == 0:
            raise NotEnoughValuesError()

        self._values = values

    def __repr__(self) -> str:
        return f"{type(self).__name__}[{self._values!r}]"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Container):
            return False

        for value in self._values:
            if value not in other:
                return False

        return True


def contains(*values: Any) -> ContainerTemplate[Any]:
    return ContainerTemplate(*values)
