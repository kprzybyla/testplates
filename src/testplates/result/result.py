__all__ = ["Result"]

import abc

from typing import TypeVar, Generic

from testplates import result

ValueType = TypeVar("ValueType")
ErrorType = TypeVar("ErrorType", bound=Exception)


class Result(abc.ABC, Generic[ValueType, ErrorType]):

    __slots__ = ()

    @property
    def is_success(self) -> bool:
        return isinstance(self, result.Success)

    @property
    def is_failure(self) -> bool:
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
