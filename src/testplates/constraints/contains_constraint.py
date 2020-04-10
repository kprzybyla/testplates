__all__ = ["contains"]

from typing import Any, TypeVar, Generic, Container, Final

import testplates

from testplates.abc import Constraint
from testplates.utils import format_like_tuple
from testplates.exceptions import InsufficientValuesError

_T = TypeVar("_T")

MINIMUM_NUMBER_OF_VALUES: Final[int] = 1


class Contains(Generic[_T], Constraint):

    __slots__ = ("_values",)

    def __init__(self, *values: _T) -> None:
        if len(values) < MINIMUM_NUMBER_OF_VALUES:
            raise InsufficientValuesError(MINIMUM_NUMBER_OF_VALUES)

        self._values = values

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{contains.__name__}({format_like_tuple(self._values)})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Container):
            return False

        for value in self._values:
            if value not in other:
                return False

        return True


def contains(*values: _T) -> Contains[_T]:
    return Contains(*values)
