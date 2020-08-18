__all__ = ["HasLength"]

from typing import Any, Sized

import testplates


class HasLength:

    __slots__ = ("_length",)

    def __init__(self, length: int, /) -> None:
        self._length = length

    def __repr__(self) -> str:
        return f"{testplates.__name__}.has_size({self._length})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Sized):
            return False

        return len(other) == self._length
