__all__ = ["matches", "format_like_dict"]

from typing import Any, TypeVar, Mapping

from .value import ANY, WILDCARD, ABSENT, MISSING, Value, Maybe

_T = TypeVar("_T")


def matches(self_value: Maybe[Value[_T]], other_value: Maybe[Value[_T]], /) -> bool:

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


def format_like_dict(mapping: Mapping[Any, Any]) -> str:
    return ", ".join((f"{key}={value!r}" for key, value in mapping.items()))
