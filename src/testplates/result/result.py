__all__ = ["Result"]

import abc

from typing import TypeVar, Protocol

ValueType = TypeVar("ValueType")
ErrorType = TypeVar("ErrorType", bound=Exception)


class Result(Protocol[ValueType, ErrorType]):

    __slots__ = ()

    @property
    @abc.abstractmethod
    def is_success(self) -> bool:

        """
            Returns True if result is a success, otherwise False.
        """

    @property
    @abc.abstractmethod
    def is_failure(self) -> bool:

        """
            Returns True if result is a failure, otherwise False.
        """
