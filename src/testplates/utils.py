__all__ = ["compare"]

from typing import TypeVar

from .abc import Missing, Value, Maybe, ANY, WILDCARD, ABSENT

T = TypeVar("T")


def compare(self_value: Maybe[Value[T]], other_value: Maybe[Value[T]]) -> bool:

    """
        Compares self value and other value and
        returns True if they match, otherwise False.

        Assumes that special values were validated
        against field types and do not bend any logic.

        :param self_value: self template value
        :param other_value: other object value
    """

    if self_value is WILDCARD:
        return True

    if self_value is ANY and other_value is not Missing:
        return True

    if self_value is ABSENT and other_value is Missing:
        return True

    return self_value == other_value
