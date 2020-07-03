__all__ = ["Result"]

import abc

from typing import TypeVar, Generic, Optional

from testplates import result

ValueType = TypeVar("ValueType")
ErrorType = TypeVar("ErrorType", bound=Exception)


class Result(abc.ABC, Generic[ValueType, ErrorType]):

    __slots__ = ("_value", "_error")

    def __init__(self, value: Optional[ValueType], error: Optional[ErrorType]) -> None:
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
    def value(self) -> ValueType:

        """
            Returns value.
        """

    @property
    @abc.abstractmethod
    def error(self) -> ErrorType:

        """
            Returns error.
        """
