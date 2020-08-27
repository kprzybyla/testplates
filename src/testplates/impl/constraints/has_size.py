__all__ = ("HasSize",)

from typing import (
    Any,
    Sized,
)

import testplates


class HasSize:

    __slots__ = (
        "name",
        "size",
    )

    def __init__(self, name: str, size: int, /) -> None:
        self.name = name
        self.size = size

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{self.name}({self.size})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Sized):
            return False

        return len(other) == self.size
