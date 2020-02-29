__all__ = ["ranges_between"]

from typing import overload, Any, TypeVar, Generic, Optional

from testplates.abc import SupportsBoundaries

from .constraint import Constraint
from .boundary import get_minimum_boundary, get_maximum_boundary, validate_boundaries

_Boundary = TypeVar("_Boundary", bound=SupportsBoundaries)


class RangeTemplate(Generic[_Boundary], Constraint):

    __slots__ = (
        "_exclusive_minimum",
        "_exclusive_maximum",
        "_inclusive_minimum",
        "_inclusive_maximum",
    )

    def __init__(
        self,
        *,
        exclusive_minimum: Optional[_Boundary] = None,
        exclusive_maximum: Optional[_Boundary] = None,
        inclusive_minimum: Optional[_Boundary] = None,
        inclusive_maximum: Optional[_Boundary] = None,
    ) -> None:
        validate_boundaries(
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
            inclusive_minimum=inclusive_minimum,
            inclusive_maximum=inclusive_maximum,
        )

        self._exclusive_minimum = exclusive_minimum
        self._exclusive_maximum = exclusive_maximum
        self._inclusive_minimum = inclusive_minimum
        self._inclusive_maximum = inclusive_maximum

    def __repr__(self) -> str:
        minimum = get_minimum_boundary(self._exclusive_minimum, self._inclusive_minimum)
        maximum = get_maximum_boundary(self._exclusive_maximum, self._inclusive_maximum)

        parameters = [
            f"{minimum.type}_{minimum.name}={minimum.value}",
            f"{maximum.type}_{maximum.name}={maximum.value}",
        ]

        return f"{type(self).__name__}[{', '.join(parameters)}]"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, SupportsBoundaries):
            return False

        if self._exclusive_minimum is not None and other <= self._exclusive_minimum:
            return False

        if self._exclusive_maximum is not None and other >= self._exclusive_maximum:
            return False

        if self._inclusive_minimum is not None and other < self._inclusive_minimum:
            return False

        if self._inclusive_maximum is not None and other > self._inclusive_maximum:
            return False

        return True


@overload
def ranges_between(
    *, exclusive_minimum: Optional[_Boundary], exclusive_maximum: Optional[_Boundary]
) -> RangeTemplate[_Boundary]:
    ...


@overload
def ranges_between(
    *, inclusive_minimum: Optional[_Boundary], inclusive_maximum: Optional[_Boundary]
) -> RangeTemplate[_Boundary]:
    ...


@overload
def ranges_between(
    *, exclusive_minimum: Optional[_Boundary], inclusive_maximum: Optional[_Boundary]
) -> RangeTemplate[_Boundary]:
    ...


@overload
def ranges_between(
    *, inclusive_minimum: Optional[_Boundary], exclusive_maximum: Optional[_Boundary]
) -> RangeTemplate[_Boundary]:
    ...


def ranges_between(
    *,
    exclusive_minimum: Optional[_Boundary] = None,
    exclusive_maximum: Optional[_Boundary] = None,
    inclusive_minimum: Optional[_Boundary] = None,
    inclusive_maximum: Optional[_Boundary] = None,
) -> RangeTemplate[_Boundary]:
    if (
        exclusive_minimum is not None
        or exclusive_maximum is not None
        or inclusive_minimum is not None
        or inclusive_maximum is not None
    ):
        return RangeTemplate(
            exclusive_minimum=exclusive_minimum,
            exclusive_maximum=exclusive_maximum,
            inclusive_minimum=inclusive_minimum,
            inclusive_maximum=inclusive_maximum,
        )

    raise TypeError("ranges_between() missing 2 required keyword-only arguments")
