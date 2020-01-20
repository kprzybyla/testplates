__all__ = ["SupportsExclusiveBoundaries", "SupportsInclusiveBoundaries", "SupportsBoundaries"]

from typing import Any
from typing_extensions import runtime_checkable, Protocol


@runtime_checkable
class SupportsExclusiveBoundaries(Protocol):
    def __gt__(self, other: Any) -> bool:
        ...

    def __lt__(self, other: Any) -> bool:
        ...


@runtime_checkable
class SupportsInclusiveBoundaries(Protocol):
    def __ge__(self, other: Any) -> bool:
        ...

    def __le__(self, other: Any) -> bool:
        ...


@runtime_checkable
class SupportsBoundaries(SupportsExclusiveBoundaries, SupportsInclusiveBoundaries, Protocol):
    def __gt__(self, other: Any) -> bool:
        ...

    def __lt__(self, other: Any) -> bool:
        ...

    def __ge__(self, other: Any) -> bool:
        ...

    def __le__(self, other: Any) -> bool:
        ...
