__all__ = ["has_unique_items"]

from typing import Iterable, Hashable


def has_unique_items(items: Iterable[Hashable]) -> bool:
    visited = set()

    for item in items:
        if item in visited:
            return False
        else:
            visited.add(item)

    return True
