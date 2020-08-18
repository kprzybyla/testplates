__all__ = ["MatchesPattern"]

import re
import abc

from typing import Any, AnyStr, Type, Generic, Pattern

import testplates


class MatchesPattern(Generic[AnyStr], abc.ABC):

    __slots__ = ("_pattern", "_pattern_type")

    def __init__(self, value: AnyStr, pattern_type: Type[AnyStr], /) -> None:
        self._pattern: Pattern[AnyStr] = re.compile(value)
        self._pattern_type: Type[AnyStr] = pattern_type

    def __repr__(self) -> str:
        return f"{testplates.__name__}.matches_pattern({self._pattern.pattern!r})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self._pattern_type):
            return False

        return bool(self._pattern.match(other))
