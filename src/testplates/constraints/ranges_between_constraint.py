__all__ = ["ranges_between"]

from typing import overload, Any, TypeVar, Generic, Optional

import testplates

from testplates.abc import Constraint

from .boundaries import get_minimum, get_maximum, validate_boundaries

_Boundary = TypeVar("_Boundary", int, float)

# TODO(kprzybyla): Remove noqa(F811) after github.com/PyCQA/pyflakes/issues/320 is released


class RangesBetween(Generic[_Boundary], Constraint):

    __slots__ = (
        "_inclusive_minimum",
        "_inclusive_maximum",
        "_exclusive_minimum",
        "_exclusive_maximum",
    )

    def __init__(
        self,
        *,
        inclusive_minimum: Optional[_Boundary] = None,
        inclusive_maximum: Optional[_Boundary] = None,
        exclusive_minimum: Optional[_Boundary] = None,
        exclusive_maximum: Optional[_Boundary] = None,
    ) -> None:
        validate_boundaries(
            inclusive_minimum=inclusive_minimum,
            inclusive_maximum=inclusive_maximum,
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
        )

        self._inclusive_minimum: Optional[_Boundary] = inclusive_minimum
        self._inclusive_maximum: Optional[_Boundary] = inclusive_maximum
        self._exclusive_minimum: Optional[_Boundary] = exclusive_minimum
        self._exclusive_maximum: Optional[_Boundary] = exclusive_maximum

    def __repr__(self) -> str:
        minimum = get_minimum(inclusive=self._inclusive_minimum, exclusive=self._exclusive_minimum)
        maximum = get_maximum(inclusive=self._inclusive_maximum, exclusive=self._exclusive_maximum)

        parameters = [
            f"{minimum.type}_{minimum.name}={minimum.value}",
            f"{maximum.type}_{maximum.name}={maximum.value}",
        ]

        return f"{testplates.__name__}.{type(self).__name__}[{', '.join(parameters)}]"

    def __eq__(self, other: Any) -> bool:
        if (
            self._inclusive_minimum is not None
            and other.__ge__(self._inclusive_minimum) is not True
        ):
            return False

        if (
            self._inclusive_maximum is not None
            and other.__le__(self._inclusive_maximum) is not True
        ):
            return False

        if (
            self._exclusive_minimum is not None
            and other.__gt__(self._exclusive_minimum) is not True
        ):
            return False

        if (
            self._exclusive_maximum is not None
            and other.__lt__(self._exclusive_maximum) is not True
        ):
            return False

        return True


@overload
def ranges_between(
    *, minimum: Optional[_Boundary], maximum: Optional[_Boundary]
) -> RangesBetween[_Boundary]:
    ...


@overload  # noqa(F811)
def ranges_between(
    *, minimum: Optional[_Boundary], exclusive_maximum: Optional[_Boundary]
) -> RangesBetween[_Boundary]:
    ...


@overload  # noqa(F811)
def ranges_between(
    *, exclusive_minimum: Optional[_Boundary], maximum: Optional[_Boundary]
) -> RangesBetween[_Boundary]:
    ...


@overload  # noqa(F811)
def ranges_between(
    *, exclusive_minimum: Optional[_Boundary], exclusive_maximum: Optional[_Boundary]
) -> RangesBetween[_Boundary]:
    ...


def ranges_between(  # noqa(F811)
    *,
    minimum: Optional[_Boundary] = None,
    maximum: Optional[_Boundary] = None,
    exclusive_minimum: Optional[_Boundary] = None,
    exclusive_maximum: Optional[_Boundary] = None,
) -> RangesBetween[_Boundary]:
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
