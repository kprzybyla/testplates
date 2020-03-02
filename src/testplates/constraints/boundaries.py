__all__ = ["get_boundary", "get_minimum", "get_maximum", "validate_boundaries"]

from typing import TypeVar, Optional
from typing_extensions import Final

from testplates.abc import Boundary
from testplates.exceptions import (
    MissingBoundaryValueError,
    MutuallyExclusiveBoundaryValueError,
    OverlappingBoundariesValueError,
    SingleMatchBoundariesValueError,
)

_T = TypeVar("_T")

MINIMUM_NAME: Final[str] = "minimum"
MAXIMUM_NAME: Final[str] = "maximum"

INCLUSIVE_NAME: Final[str] = "inclusive"
EXCLUSIVE_NAME: Final[str] = "exclusive"

INCLUSIVE_ALIGNMENT: Final[int] = 0
EXCLUSIVE_ALIGNMENT: Final[int] = 1


class Inclusive(Boundary[_T]):

    __slots__ = ()

    @property
    def type(self) -> str:
        return INCLUSIVE_NAME

    @property
    def alignment(self) -> int:
        return INCLUSIVE_ALIGNMENT


class Exclusive(Boundary[_T]):

    __slots__ = ()

    @property
    def type(self) -> str:
        return EXCLUSIVE_NAME

    @property
    def alignment(self) -> int:
        return EXCLUSIVE_ALIGNMENT


def get_boundary(
    name: str, *, inclusive: Optional[_T] = None, exclusive: Optional[_T] = None
) -> Boundary[_T]:
    if inclusive is None and exclusive is None:
        raise MissingBoundaryValueError(name)

    if inclusive is not None and exclusive is not None:
        raise MutuallyExclusiveBoundaryValueError(name)

    return Inclusive(name, inclusive) or Exclusive(name, exclusive)


def get_minimum(*, inclusive: Optional[_T] = None, exclusive: Optional[_T] = None) -> Boundary[_T]:
    return get_boundary(MINIMUM_NAME, inclusive=inclusive, exclusive=exclusive)


def get_maximum(*, inclusive: Optional[_T] = None, exclusive: Optional[_T] = None) -> Boundary[_T]:
    return get_boundary(MAXIMUM_NAME, inclusive=inclusive, exclusive=exclusive)


def validate_boundaries(
    *,
    inclusive_minimum: Optional[_T] = None,
    inclusive_maximum: Optional[_T] = None,
    exclusive_minimum: Optional[_T] = None,
    exclusive_maximum: Optional[_T] = None,
) -> None:
    minimum = get_minimum(inclusive=inclusive_minimum, exclusive=exclusive_minimum)
    maximum = get_maximum(inclusive=inclusive_maximum, exclusive=exclusive_maximum)

    if minimum.value + minimum.alignment > maximum.value - maximum.alignment:
        raise OverlappingBoundariesValueError(minimum, maximum)

    if minimum.value + minimum.alignment == maximum.value - maximum.alignment:
        raise SingleMatchBoundariesValueError(minimum, maximum)
