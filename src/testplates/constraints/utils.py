__all__ = ["format_like_tuple"]

from typing import Any, Iterable


def format_like_tuple(values: Iterable[Any]) -> str:
    return ", ".join((repr(value) for value in values))
