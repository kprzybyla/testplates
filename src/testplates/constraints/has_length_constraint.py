__all__ = ["has_length"]

import abc

from typing import overload, Any, Sized, Optional

import testplates

from testplates.abc import Constraint

from .boundaries import get_length_boundaries

# TODO(kprzybyla): Remove noqa(F811) after github.com/PyCQA/pyflakes/issues/320 is released


class AnyHasLength(Constraint, abc.ABC):

    __slots__ = ()

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Sized)


class HasLength(AnyHasLength):

    __slots__ = ("_length",)

    def __init__(self, length: int) -> None:
        self._length = length

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{type(self).__name__}[{self._length}]"

    def __eq__(self, other: Any) -> bool:
        if not super().__eq__(other):
            return False

        return len(other) == self._length


class HasLengthBetween(AnyHasLength):

    __slots__ = ("_minimum", "_maximum")

    def __init__(
        self, *, inclusive_minimum: Optional[int] = None, inclusive_maximum: Optional[int] = None
    ) -> None:
        minimum, maximum = get_length_boundaries(
            inclusive_minimum=inclusive_minimum, inclusive_maximum=inclusive_maximum
        )

        self._minimum = minimum
        self._maximum = maximum

    def __repr__(self) -> str:
        parameters = [
            repr(self._minimum),
            repr(self._maximum),
        ]

        return f"{testplates.__name__}.{type(self).__name__}[{', '.join(parameters)}]"

    def __eq__(self, other: Any) -> bool:
        if not super().__eq__(other):
            return False

        return self._minimum.fits(len(other)) and self._maximum.fits(len(other))


@overload
def has_length(length: int) -> HasLength:
    ...


@overload  # noqa(F811)
def has_length(*, minimum: int, maximum: int) -> HasLengthBetween:
    ...


def has_length(  # noqa(F811)
    length: Optional[int] = None, *, minimum: Optional[int] = None, maximum: Optional[int] = None
) -> AnyHasLength:
    if length is not None:
        return HasLength(length)

    if minimum is not None or maximum is not None:
        return HasLengthBetween(inclusive_minimum=minimum, inclusive_maximum=maximum)

    raise TypeError("has_length() missing 1 positional argument or 2 keyword-only arguments")
