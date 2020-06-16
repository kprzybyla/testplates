__all__ = ["Boundary", "LiteralBoundary"]

import abc

from typing import TypeVar, Generic, Union, Literal

_T = TypeVar("_T", bound=Union[int, float])


class Boundary(Generic[_T], abc.ABC):

    """
        Abstract boundary class.
    """

    __slots__ = ()

    def __repr__(self) -> str:
        return type(self).__name__

    @abc.abstractmethod
    def fits(self, value: _T, /) -> bool:

        """
            Returns True if value fits within boundary, otherwise False.

            :param value: value to be validated
        """


class LiteralBoundary(Boundary[_T], Generic[_T], abc.ABC):

    """
        Abstract literal boundary class.
    """

    __slots__ = ("_value",)

    def __init__(self, value: _T) -> None:
        self._value: _T = value

    def __repr__(self) -> str:
        return f"{self.type}_{self.name}={self.value}"

    @property
    def value(self) -> _T:

        """
            Returns boundary value.
        """

        return self._value

    @property
    @abc.abstractmethod
    def name(self) -> str:

        """
            Returns boundary name.
        """

    @property
    @abc.abstractmethod
    def type(self) -> str:

        """
            Returns boundary type name.
        """

    @property
    @abc.abstractmethod
    def alignment(self) -> Literal[0, 1]:

        """
            Returns boundary alignment.

            Alignment indicates whether we accept the value
            equal to the boundary as correct one or not.

            If alignment is equal to 0, value equal to boundary is accepted.
            If alignment is equal to 1, value equal to boundary is not accepted.
        """
