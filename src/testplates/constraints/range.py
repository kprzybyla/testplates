__all__ = ["ranges"]

from typing import Any, TypeVar, Generic, Optional

from testplates.abc import SupportsBoundaries
from testplates.exceptions import MutuallyExclusiveBoundaryValueError

from .constraint import Constraint

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
        self._exclusive_minimum = exclusive_minimum
        self._exclusive_maximum = exclusive_maximum
        self._inclusive_minimum = inclusive_minimum
        self._inclusive_maximum = inclusive_maximum

        if self._exclusive_minimum is not None and self._inclusive_minimum is not None:
            raise MutuallyExclusiveBoundaryValueError()

        if self._exclusive_maximum is not None and self._inclusive_maximum is not None:
            raise MutuallyExclusiveBoundaryValueError()

    def __repr__(self) -> str:
        parameters = [
            f"exclusive_minimum={self._exclusive_minimum}",
            f"exclusive_maximum={self._exclusive_maximum}",
            f"inclusive_minimum={self._inclusive_minimum}",
            f"inclusive_maximum={self._inclusive_maximum}",
        ]

        return f"{type(self).__name__}[{', '.join(parameters)}]"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, SupportsBoundaries):
            return False

        if self._exclusive_minimum is not None and other < self._exclusive_minimum:
            return False

        if self._exclusive_maximum is not None and other > self._exclusive_maximum:
            return False

        if self._inclusive_minimum is not None and other <= self._inclusive_minimum:
            return False

        if self._inclusive_maximum is not None and other >= self._inclusive_maximum:
            return False

        return True


def ranges(
    *,
    exclusive_minimum: Optional[_Boundary] = None,
    exclusive_maximum: Optional[_Boundary] = None,
    inclusive_minimum: Optional[_Boundary] = None,
    inclusive_maximum: Optional[_Boundary] = None,
) -> RangeTemplate[_Boundary]:
    return RangeTemplate(
        exclusive_minimum=exclusive_minimum,
        exclusive_maximum=exclusive_maximum,
        inclusive_minimum=inclusive_minimum,
        inclusive_maximum=inclusive_maximum,
    )
