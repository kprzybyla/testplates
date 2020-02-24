__all__ = ["get_boundary", "get_minimum_boundary", "get_maximum_boundary", "validate_boundaries"]

from typing import TypeVar, Optional
from typing_extensions import Final

from testplates.abc import Boundary
from testplates.exceptions import (
    MissingBoundaryValueError,
    MutuallyExclusiveBoundaryValueError,
    OverlappingBoundariesValueError,
)

_T = TypeVar("_T")

MINIMUM_NAME: Final[str] = "minimum"
MAXIMUM_NAME: Final[str] = "maximum"

EXCLUSIVE_NAME: Final[str] = "exclusive"
INCLUSIVE_NAME: Final[str] = "inclusive"

EXCLUSIVE_ALIGNMENT: Final[int] = 1
INCLUSIVE_ALIGNMENT: Final[int] = 0


class Exclusive(Boundary[_T]):

    __slots__ = ()

    @property
    def type(self) -> str:
        return EXCLUSIVE_NAME

    @property
    def alignment(self) -> int:
        return EXCLUSIVE_ALIGNMENT


class Inclusive(Boundary[_T]):

    __slots__ = ()

    @property
    def type(self) -> str:
        return INCLUSIVE_NAME

    @property
    def alignment(self) -> int:
        return INCLUSIVE_ALIGNMENT


def get_boundary(
    name: str, exclusive: Optional[_T] = None, inclusive: Optional[_T] = None
) -> Boundary[_T]:
    if exclusive is None and inclusive is None:
        raise MissingBoundaryValueError(name)

    if exclusive is not None and inclusive is not None:
        raise MutuallyExclusiveBoundaryValueError(name)

    return Exclusive(name, exclusive) or Inclusive(name, inclusive)


def get_minimum_boundary(
    exclusive: Optional[_T] = None, inclusive: Optional[_T] = None
) -> Boundary[_T]:
    return get_boundary(MINIMUM_NAME, exclusive=exclusive, inclusive=inclusive)


def get_maximum_boundary(
    exclusive: Optional[_T] = None, inclusive: Optional[_T] = None
) -> Boundary[_T]:
    return get_boundary(MAXIMUM_NAME, exclusive=exclusive, inclusive=inclusive)


def validate_boundaries(
    *,
    exclusive_minimum: Optional[_T] = None,
    exclusive_maximum: Optional[_T] = None,
    inclusive_minimum: Optional[_T] = None,
    inclusive_maximum: Optional[_T] = None,
) -> None:
    minimum = get_minimum_boundary(exclusive_minimum, inclusive_minimum)
    maximum = get_maximum_boundary(exclusive_maximum, inclusive_maximum)

    if minimum.value + minimum.alignment > maximum.value - maximum.alignment:
        raise OverlappingBoundariesValueError(minimum, maximum)
