__all__ = ["Boundary"]

import abc

from typing import TypeVar, Generic, Union
from typing_extensions import Literal

from .protocols import SupportsAddition, SupportsSubtraction

_T = TypeVar("_T", SupportsAddition, SupportsSubtraction)


class Boundary(Generic[_T], abc.ABC):

    __slots__ = ("_value",)

    def __init__(self, value: _T) -> None:
        self._value = value

    def __bool__(self) -> bool:
        return self._value is not None

    @property
    def value(self) -> _T:

        """
            Returns boundary value.
        """

        return self._value

    @property
    @abc.abstractmethod
    def type(self) -> str:

        """
            Returns boundary type name.
        """

    @property
    @abc.abstractmethod
    def alignment(self) -> Union[Literal[0], Literal[1]]:

        """
            Returns boundary alignment.

            Alignment indicates whether we accept the value
            equal to the boundary as correct one or not.

            If alignment is equal to 0, value equal to boundary is accepted.
            If alignment is equal to 1, value equal to boundary is not accepted.
        """
