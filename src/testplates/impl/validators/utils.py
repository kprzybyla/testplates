__all__ = ["has_unique_items", "Validator"]

from typing import Any, Iterable, Hashable, Callable

from testplates.impl.base import Result

from .exceptions import ValidationError

Validator = Callable[[Any], Result[None, ValidationError]]


def has_unique_items(items: Iterable[Hashable]) -> bool:
    visited = set()

    for item in items:
        if item in visited:
            return False
        else:
            visited.add(item)

    return True
