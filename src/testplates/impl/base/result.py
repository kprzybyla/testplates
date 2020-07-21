from __future__ import annotations

__all__ = ["Result", "Success", "Failure"]

import abc

from typing import Any, TypeVar, Generic

import testplates

ValueType = TypeVar("ValueType")
ErrorType = TypeVar("ErrorType", bound=Exception)


class Result(Generic[ValueType, ErrorType], abc.ABC):

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


class Success(Result[ValueType, Any], Generic[ValueType]):

    __slots__ = ("_value",)

    def __init__(self, value: ValueType) -> None:
        self._value = value

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{type(self).__name__}({self.value})"

    @classmethod
    def from_result(cls, result: Result[ValueType, Any]) -> Success[ValueType]:

        """
            Returns success from result.

            :param result: result from which success is created
        """

        assert isinstance(result, Success), result
        return result

    @classmethod
    def get_value(cls, result: Result[ValueType, Any]) -> ValueType:

        """
            Returns value from result.

            :param result: result from which value is extracted
        """

        return cls.from_result(result).value

    @property
    def is_success(self) -> bool:
        return True

    @property
    def is_failure(self) -> bool:
        return False

    @property
    def value(self) -> ValueType:
        return self._value


class Failure(Result[Any, ErrorType], Generic[ErrorType]):

    __slots__ = ("_error",)

    def __init__(self, error: ErrorType) -> None:
        self._error = error

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{type(self).__name__}({self.error})"

    @classmethod
    def from_result(cls, result: Result[Any, ErrorType]) -> Failure[ErrorType]:

        """
            Returns failure from result.

            :param result: result from which failure is created
        """

        assert isinstance(result, Failure), result
        return result

    @classmethod
    def get_error(cls, result: Result[Any, ErrorType]) -> ErrorType:

        """
            Returns error from result.

            :param result: result from which error is extracted
        """

        return cls.from_result(result).error

    @property
    def is_success(self) -> bool:
        return False

    @property
    def is_failure(self) -> bool:
        return True

    @property
    def error(self) -> ErrorType:
        return self._error
