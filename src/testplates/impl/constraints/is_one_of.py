__all__ = ["IsOneOf"]

from typing import Any, TypeVar, Generic, Final

import testplates

from testplates.impl.utils import format_like_tuple

from .exceptions import InsufficientValuesError

_T = TypeVar("_T")

MINIMUM_NUMBER_OF_VALUES: Final[int] = 2


class IsOneOf(Generic[_T]):

    __slots__ = ("values",)

    def __init__(self, *values: _T) -> None:
        if len(values) < MINIMUM_NUMBER_OF_VALUES:
            raise InsufficientValuesError(MINIMUM_NUMBER_OF_VALUES)

        self.values = values

    def __repr__(self) -> str:
        return f"{testplates.__name__}.is_one_of({format_like_tuple(self.values)})"

    def __eq__(self, other: Any) -> bool:
        return other in self.values
