__all__ = ["compare"]

from typing import TypeVar

from .abc import Missing, Value, Maybe, ANY, WILDCARD, ABSENT

T = TypeVar("T")


def compare(self_value: Maybe[Value[T]], other_value: Maybe[Value[T]]) -> bool:
    if self_value is WILDCARD:
        return True

    if other_value is not Missing and self_value is ANY:
        return True

    if other_value is Missing and self_value is ABSENT:
        return True

    return self_value == other_value
