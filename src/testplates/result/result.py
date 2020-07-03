__all__ = ["Result"]

import abc

from typing import TypeVar, Generic, Optional

from testplates import result

_T = TypeVar("_T")
_E = TypeVar("_E", bound=Exception)


class Result(Generic[_T, _E], abc.ABC):

    __slots__ = ("_value", "_error")

    def __init__(self, value: Optional[_T], error: Optional[_E]) -> None:
        self._value = value
        self._error = error

    @property
    def is_value(self) -> bool:
        return isinstance(self, result.Success)

    @property
    def is_error(self) -> bool:
        return isinstance(self, result.Failure)

    @property
    @abc.abstractmethod
    def value(self) -> _T:

        """
            ...
        """

    @property
    @abc.abstractmethod
    def error(self) -> _E:

        """
            ...
        """
