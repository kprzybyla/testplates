__all__ = ["Limit"]

from typing import TypeVar, Generic, Literal, Final

_T = TypeVar("_T", int, float)

INCLUSIVE_ALIGNMENT: Final[Literal[0]] = 0
EXCLUSIVE_ALIGNMENT: Final[Literal[1]] = 1


class Limit(Generic[_T]):

    __slots__ = ("_name", "_value", "_is_inclusive")

    def __init__(self, name: str, value: _T, *, is_inclusive: bool) -> None:
        self._name = name
        self._value = value
        self._is_inclusive = is_inclusive

    def __repr__(self) -> str:
        prefix = "" if self.is_inclusive else "exclusive_"

        return f"{prefix}{self.name}={self.value}"

    @property
    def name(self) -> str:

        """
            Returns limit name.
        """

        return self._name

    @property
    def value(self) -> _T:

        """
            Returns limit value.
        """

        return self._value

    @property
    def is_inclusive(self) -> bool:

        """
            Returns True if limit is inclusive, otherwise False.
        """

        return self._is_inclusive

    @property
    def alignment(self) -> Literal[0, 1]:

        """
            Returns limit alignment.

            Alignment indicates whether we accept the value
            equal to the limit value as correct one or not.

            If alignment is equal to 0, value equal to limit is accepted.
            If alignment is equal to 1, value equal to limit is not accepted.
        """

        return INCLUSIVE_ALIGNMENT if self.is_inclusive else EXCLUSIVE_ALIGNMENT
