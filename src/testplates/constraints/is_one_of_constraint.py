__all__ = ["is_one_of"]

from typing import Any, TypeVar, Generic
from typing_extensions import Final

import testplates

from testplates.abc import Constraint
from testplates.exceptions import TooLittleValuesError

_T = TypeVar("_T", covariant=True)

MINIMUM_NUMBER_OF_VALUES: Final[int] = 2


class IsOneOf(Generic[_T], Constraint):

    __slots__ = ("_values",)

    def __init__(self, *values: _T) -> None:
        if len(values) < MINIMUM_NUMBER_OF_VALUES:
            raise TooLittleValuesError(MINIMUM_NUMBER_OF_VALUES)

        self._values = values

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{type(self).__name__}{list(self._values)!r}"

    def __eq__(self, other: Any) -> bool:
        return other in self._values


def is_one_of(*values: Any) -> IsOneOf[Any]:
    return IsOneOf(*values)
