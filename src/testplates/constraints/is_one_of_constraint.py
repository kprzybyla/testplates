__all__ = ["is_one_of"]

from typing import Any, TypeVar, Generic, Final

import testplates

from testplates.abc import Constraint
from testplates.utils import format_like_tuple
from testplates.exceptions import InsufficientValuesError

_T = TypeVar("_T")

MINIMUM_NUMBER_OF_VALUES: Final[int] = 2


class IsOneOf(Generic[_T], Constraint):

    __slots__ = ("_values",)

    def __init__(self, *values: _T) -> None:
        if len(values) < MINIMUM_NUMBER_OF_VALUES:
            raise InsufficientValuesError(MINIMUM_NUMBER_OF_VALUES)

        self._values = values

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{is_one_of.__name__}({format_like_tuple(self._values)})"

    def __eq__(self, other: Any) -> bool:
        return other in self._values


def is_one_of(*values: _T) -> IsOneOf[_T]:
    return IsOneOf(*values)
