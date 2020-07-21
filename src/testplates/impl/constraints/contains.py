__all__ = ["Contains"]

from typing import Any, TypeVar, Generic, Container, Final

import testplates

from testplates.impl.utils import format_like_tuple
from testplates.impl.exceptions import InsufficientValuesError

T = TypeVar("T")

MINIMUM_NUMBER_OF_VALUES: Final[int] = 1


class Contains(Generic[T]):

    __slots__ = ("_values",)

    def __init__(self, *values: T) -> None:
        if len(values) < MINIMUM_NUMBER_OF_VALUES:
            raise InsufficientValuesError(MINIMUM_NUMBER_OF_VALUES)

        self._values = values

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{type(self).__name__}({format_like_tuple(self._values)})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Container):
            return False

        for value in self._values:
            if value not in other:
                return False

        return True
