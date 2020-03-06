__all__ = ["Boundary"]

import abc

from typing import TypeVar, Generic

_T = TypeVar("_T", int, float)


class Boundary(Generic[_T], abc.ABC):

    __slots__ = ("_name", "_value")

    def __init__(self, name: str, value: _T) -> None:
        self._name = name
        self._value: _T = value

    def __repr__(self) -> str:
        return f"{self.type}_{self.name}({self.value})"

    def __bool__(self) -> bool:
        return self._value is not None

    @property
    def value(self) -> _T:

        """
            Returns boundary value.
        """

        return self._value

    @property
    def name(self) -> str:

        """
            Returns boundary name.
        """

        return self._name

    @property
    @abc.abstractmethod
    def type(self) -> str:

        """
            Returns boundary type name.
        """

    @property
    @abc.abstractmethod
    def alignment(self) -> int:

        """
            Returns boundary alignment.

            Alignment indicates whether we accept the value
            equal to the boundary as correct one or not.

            If alignment is equal to 0, value equal to boundary is accepted.
            If alignment is equal to 1, value equal to boundary is not accepted.
        """
