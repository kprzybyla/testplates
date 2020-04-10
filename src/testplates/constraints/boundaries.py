__all__ = [
    "get_minimum",
    "get_maximum",
    "get_boundaries",
    "get_length_boundaries",
    "Inclusive",
    "Exclusive",
]

import sys

from typing import TypeVar, Tuple, Optional, Final

from testplates.abc import Boundary
from testplates.exceptions import (
    MissingBoundaryError,
    InvalidLengthError,
    MutuallyExclusiveBoundariesError,
    OverlappingBoundariesError,
    SingleMatchBoundariesError,
    UnreachableCodeExecutionInternalError,
)

_T = TypeVar("_T", int, float)

MINIMUM_NAME: Final[str] = "minimum"
MAXIMUM_NAME: Final[str] = "maximum"

INCLUSIVE_NAME: Final[str] = "inclusive"
EXCLUSIVE_NAME: Final[str] = "exclusive"

INCLUSIVE_ALIGNMENT: Final[int] = 0
EXCLUSIVE_ALIGNMENT: Final[int] = 1

LENGTH_MINIMUM: Final[int] = 0
LENGTH_MAXIMUM: Final[int] = sys.maxsize


class Inclusive(Boundary[_T]):

    __slots__ = ()

    def __repr__(self) -> str:
        return f"{self.name}={self.value}"

    @property
    def type(self) -> str:
        return INCLUSIVE_NAME

    @property
    def alignment(self) -> int:
        return INCLUSIVE_ALIGNMENT

    def fits(self, value: _T, /) -> bool:
        if self.name == MINIMUM_NAME and value.__ge__(self.value) is not True:
            return False

        if self.name == MAXIMUM_NAME and value.__le__(self.value) is not True:
            return False

        return True


class Exclusive(Boundary[_T]):

    __slots__ = ()

    def __repr__(self) -> str:
        return f"{self.type}_{self.name}={self.value}"

    @property
    def type(self) -> str:
        return EXCLUSIVE_NAME

    @property
    def alignment(self) -> int:
        return EXCLUSIVE_ALIGNMENT

    def fits(self, value: _T, /) -> bool:
        if self.name == MINIMUM_NAME and value.__gt__(self.value) is not True:
            return False

        if self.name == MAXIMUM_NAME and value.__lt__(self.value) is not True:
            return False

        return True


def get_minimum(*, inclusive: Optional[_T] = None, exclusive: Optional[_T] = None) -> Boundary[_T]:
    return _get_boundary(MINIMUM_NAME, inclusive=inclusive, exclusive=exclusive)


def get_maximum(*, inclusive: Optional[_T] = None, exclusive: Optional[_T] = None) -> Boundary[_T]:
    return _get_boundary(MAXIMUM_NAME, inclusive=inclusive, exclusive=exclusive)


def get_boundaries(
    *,
    inclusive_minimum: Optional[_T] = None,
    inclusive_maximum: Optional[_T] = None,
    exclusive_minimum: Optional[_T] = None,
    exclusive_maximum: Optional[_T] = None,
) -> Tuple[Boundary[_T], Boundary[_T]]:
    minimum = get_minimum(inclusive=inclusive_minimum, exclusive=exclusive_minimum)
    maximum = get_maximum(inclusive=inclusive_maximum, exclusive=exclusive_maximum)

    if minimum.value + minimum.alignment > maximum.value - maximum.alignment:
        raise OverlappingBoundariesError(minimum, maximum)

    if minimum.value + minimum.alignment == maximum.value - maximum.alignment:
        raise SingleMatchBoundariesError(minimum, maximum)

    return minimum, maximum


def get_length_boundaries(
    *, inclusive_minimum: Optional[int] = None, inclusive_maximum: Optional[int] = None
) -> Tuple[Boundary[int], Boundary[int]]:
    minimum = get_minimum(inclusive=inclusive_minimum)
    maximum = get_maximum(inclusive=inclusive_maximum)

    if minimum.value < LENGTH_MINIMUM or minimum.value > LENGTH_MAXIMUM:
        raise InvalidLengthError(minimum)

    if maximum.value < LENGTH_MINIMUM or maximum.value > LENGTH_MAXIMUM:
        raise InvalidLengthError(maximum)

    if minimum.value + minimum.alignment > maximum.value - maximum.alignment:
        raise OverlappingBoundariesError(minimum, maximum)

    if minimum.value + minimum.alignment == maximum.value - maximum.alignment:
        raise SingleMatchBoundariesError(minimum, maximum)

    return minimum, maximum


def _get_boundary(
    name: str, /, *, inclusive: Optional[_T] = None, exclusive: Optional[_T] = None
) -> Boundary[_T]:
    if inclusive is None and exclusive is None:
        raise MissingBoundaryError(name)

    if inclusive is not None and exclusive is not None:
        raise MutuallyExclusiveBoundariesError(name)

    if inclusive is not None:
        return Inclusive(name, inclusive)

    if exclusive is not None:
        return Exclusive(name, exclusive)

    raise UnreachableCodeExecutionInternalError()  # pragma: no cover
