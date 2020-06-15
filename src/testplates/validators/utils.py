__all__ = ["validate_any", "has_unique_items", "Result", "Validator"]

from typing import Any, TypeVar, Union, Iterable, Hashable, Callable, Optional

_T = TypeVar("_T")

Result = Union[_T, Exception]
Validator = Callable[[_T], Optional[Exception]]


# noinspection PyUnusedLocal
def validate_any(data: Any) -> Optional[Exception]:
    return None


def has_unique_items(items: Iterable[Hashable]) -> bool:
    visited = set()

    for item in items:
        if item in visited:
            return False
        else:
            visited.add(item)

    return True
