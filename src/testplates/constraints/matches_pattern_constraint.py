__all__ = ["matches_pattern"]

import re
import abc

from typing import Any, AnyStr, Type, Generic, Pattern

import testplates

from testplates.abc import Constraint


class MatchesPattern(Generic[AnyStr], Constraint, abc.ABC):

    __slots__ = ("_pattern", "_pattern_type")

    def __init__(self, value: AnyStr, /, pattern_type: Type[AnyStr]) -> None:
        self._pattern: Pattern[AnyStr] = re.compile(value)
        self._pattern_type: Type[AnyStr] = pattern_type

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{matches_pattern.__name__}({self._pattern.pattern!r})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self._pattern_type):
            return False

        return bool(self._pattern.match(other))


def matches_pattern(pattern: AnyStr, /) -> MatchesPattern[AnyStr]:

    """
        Returns constraint object that matches any string
        object whose content matches the specified pattern.

        :param pattern: pattern to be matched inside string content
    """

    if isinstance(pattern, str):
        return MatchesPattern(pattern, str)

    if isinstance(pattern, bytes):
        return MatchesPattern(pattern, bytes)

    raise TypeError("matches() requires str or bytes as 1st argument")
