__all__ = ["ranges_between"]

from typing import overload, Any, TypeVar, Generic, Optional

import testplates

from testplates.abc import Boundary, Constraint

from .boundaries import get_boundaries

_T = TypeVar("_T", int, float)


class RangesBetween(Generic[_T], Constraint):

    __slots__ = ("_minimum", "_maximum")

    def __init__(
        self,
        *,
        inclusive_minimum: Optional[_T] = None,
        inclusive_maximum: Optional[_T] = None,
        exclusive_minimum: Optional[_T] = None,
        exclusive_maximum: Optional[_T] = None,
    ) -> None:
        minimum, maximum = get_boundaries(
            inclusive_minimum=inclusive_minimum,
            inclusive_maximum=inclusive_maximum,
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )

        self._minimum: Boundary[_T] = minimum
        self._maximum: Boundary[_T] = maximum

    def __repr__(self) -> str:
        parameters = [
            repr(self._minimum),
            repr(self._maximum),
        ]

        return f"{testplates.__name__}.{type(self).__name__}[{', '.join(parameters)}]"

    def __eq__(self, other: Any) -> bool:
        return self._minimum.fits(other) and self._maximum.fits(other)


@overload
def ranges_between(*, minimum: Optional[_T], maximum: Optional[_T]) -> RangesBetween[_T]:
    ...


@overload
def ranges_between(*, minimum: Optional[_T], exclusive_maximum: Optional[_T]) -> RangesBetween[_T]:
    ...


@overload
def ranges_between(*, exclusive_minimum: Optional[_T], maximum: Optional[_T]) -> RangesBetween[_T]:
    ...


@overload
def ranges_between(
    *, exclusive_minimum: Optional[_T], exclusive_maximum: Optional[_T]
) -> RangesBetween[_T]:
    ...


def ranges_between(
    *,
    minimum: Optional[_T] = None,
    maximum: Optional[_T] = None,
    exclusive_minimum: Optional[_T] = None,
    exclusive_maximum: Optional[_T] = None,
) -> RangesBetween[_T]:
    if (
        minimum is not None
        or maximum is not None
        or exclusive_minimum is not None
        or exclusive_maximum is not None
    ):
        return RangesBetween(
            inclusive_minimum=minimum,
            inclusive_maximum=maximum,
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )

    raise TypeError("ranges_between() missing 2 required keyword-only arguments")
