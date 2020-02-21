__all__ = ["matches"]

import re
import abc

from typing import AnyStr, Type, Generic, Pattern

from .constraint import Constraint


class AnyPatternTemplate(Generic[AnyStr], Constraint, abc.ABC):

    __slots__ = ("_pattern",)

    def __init__(self, value: AnyStr) -> None:
        self._pattern: Pattern[AnyStr] = re.compile(value)

    def __repr__(self) -> str:
        return f"{type(self).__name__}[{self._pattern.pattern}]"

    def __eq__(self, other: AnyStr) -> bool:
        if not isinstance(other, self.pattern_type):
            return False

        return bool(self._pattern.match(other))

    @property
    @abc.abstractmethod
    def pattern_type(self) -> Type[AnyStr]:

        """
            Returns pattern type class.
        """


class StringPatternTemplate(AnyPatternTemplate[str]):

    __slots__ = ()

    @property
    def pattern_type(self) -> Type[str]:
        return str


class BytesPatternTemplate(AnyPatternTemplate[bytes]):

    __slots__ = ()

    @property
    def pattern_type(self) -> Type[bytes]:
        return bytes


def matches(pattern: AnyStr) -> AnyPatternTemplate[AnyStr]:
    if isinstance(pattern, str):
        return StringPatternTemplate(pattern)

    if isinstance(pattern, bytes):
        return BytesPatternTemplate(pattern)

    raise TypeError("matches() takes str or bytes as 1st argument")
