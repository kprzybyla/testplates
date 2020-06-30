__all__ = ["has_unique_items", "Validator"]

from typing import TypeVar, Iterable, Hashable, Callable

from testplates.result import Result

_T = TypeVar("_T")

Validator = Callable[[_T], Result[None]]


def has_unique_items(items: Iterable[Hashable]) -> bool:
    visited = set()

    for item in items:
        if item in visited:
            return False
        else:
            visited.add(item)

    return True
