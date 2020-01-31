__all__ = ["matches"]

from typing import TypeVar

from .value import ANY, WILDCARD, ABSENT, MISSING, Value, Maybe

T = TypeVar("T")


def matches(self_value: Maybe[Value[T]], other_value: Maybe[Value[T]]) -> bool:

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

    if self_value is ANY and other_value is not MISSING:
        return True

    if self_value is ABSENT and other_value is MISSING:
        return True

    return self_value == other_value
