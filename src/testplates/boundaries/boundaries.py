__all__ = [
    "Unlimited",
    "InclusiveMinimum",
    "InclusiveMaximum",
    "ExclusiveMinimum",
    "ExclusiveMaximum",
]

from typing import TypeVar, Literal, Final

from testplates.abc import Boundary, LiteralBoundary

_T = TypeVar("_T", int, float)

MINIMUM_NAME: Final[str] = "minimum"
MAXIMUM_NAME: Final[str] = "maximum"

INCLUSIVE_NAME: Final[str] = "inclusive"
EXCLUSIVE_NAME: Final[str] = "exclusive"
UNLIMITED_NAME: Final[str] = "unlimited"

INCLUSIVE_ALIGNMENT: Final[Literal[0]] = 0
EXCLUSIVE_ALIGNMENT: Final[Literal[1]] = 1


class Unlimited(Boundary[_T]):

    __slots__ = ()

    def fits(self, value: _T, /) -> bool:
        return True


class InclusiveMinimum(LiteralBoundary[_T]):

    __slots__ = ()

    name = MINIMUM_NAME
    type = INCLUSIVE_NAME
    alignment = INCLUSIVE_ALIGNMENT

    def fits(self, value: _T, /) -> bool:
        return value.__ge__(self.value) is True


class InclusiveMaximum(LiteralBoundary[_T]):

    __slots__ = ()

    name = MAXIMUM_NAME
    type = INCLUSIVE_NAME
    alignment = INCLUSIVE_ALIGNMENT

    def fits(self, value: _T, /) -> bool:
        return value.__le__(self.value) is True


class ExclusiveMinimum(LiteralBoundary[_T]):

    __slots__ = ()

    name = MINIMUM_NAME
    type = EXCLUSIVE_NAME
    alignment = EXCLUSIVE_ALIGNMENT

    def fits(self, value: _T, /) -> bool:
        return value.__lt__(self.value) is True


class ExclusiveMaximum(LiteralBoundary[_T]):

    __slots__ = ()

    name = MAXIMUM_NAME
    type = EXCLUSIVE_NAME
    alignment = EXCLUSIVE_ALIGNMENT

    def fits(self, value: _T, /) -> bool:
        return value.__gt__(self.value) is True
