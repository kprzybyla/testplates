__all__ = ["HasLength"]

from typing import Any, Sized

import testplates


class HasLength:

    __slots__ = ("name", "length")

    def __init__(self, name: str, length: int, /) -> None:
        self.name = name
        self.length = length

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{self.name}({self.length})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Sized):
            return False

        return len(other) == self.length
