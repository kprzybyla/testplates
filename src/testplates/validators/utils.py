__all__ = ["validate_any", "has_unique_items", "Validator"]

from typing import Any, TypeVar, Iterable, Hashable, Callable

from testplates.result import Result, Success

_T = TypeVar("_T")

Validator = Callable[[_T], Result[Exception]]


# noinspection PyUnusedLocal
def validate_any(data: Any) -> Result[None]:
    return Success(None)


def has_unique_items(items: Iterable[Hashable]) -> bool:
    visited = set()

    for item in items:
        if item in visited:
            return False
        else:
            visited.add(item)

    return True
