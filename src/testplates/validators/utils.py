__all__ = ["has_unique_items"]

from typing import Sequence, Hashable


def has_unique_items(items: Sequence[Hashable]) -> bool:
    visited = set()

    return not any(item in visited or visited.add(item) for item in items)
