__all__ = ["has_length"]

from typing import Any, Sized

import testplates

from testplates.abc import Constraint


class HasLength(Constraint):

    __slots__ = ("_length",)

    def __init__(self, length: int, /) -> None:
        self._length = length

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{has_length.__name__}({self._length})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Sized):
            return False

        return len(other) == self._length


def has_length(length: int) -> HasLength:

    """
        Returns constraint object that matches any sized
        object that has length equal to the exact value.

        :param length: exact length value
    """

    return HasLength(length)
