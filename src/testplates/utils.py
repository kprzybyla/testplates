__all__ = ["matches", "format_like_tuple", "format_like_dict"]

from typing import Any, TypeVar, Iterable, Mapping

from testplates.base.value import Value, Maybe, ANY, WILDCARD, ABSENT, MISSING

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


def format_like_tuple(values: Iterable[Any]) -> str:

    """
        Formats iterable into tuple-like format
        that is readable for human being.

        :param values: values to be formatted
    """

    return ", ".join((repr(value) for value in values))


def format_like_dict(mapping: Mapping[Any, Any]) -> str:

    """
        Formats mapping into dict-like format
        that is readable for human being.

        :param mapping: values to be formatted
    """

    return ", ".join((f"{key}={value!r}" for key, value in mapping.items()))
