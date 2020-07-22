__all__ = ["success", "failure", "unwrap_success", "unwrap_failure", "Result"]

import abc

from typing import Any, TypeVar, Union, Protocol

from testplates.impl.base import Success, Failure

ValueType = TypeVar("ValueType", covariant=True)
ErrorType = TypeVar("ErrorType", bound=Exception, covariant=True)


class Result(Protocol[ValueType, ErrorType]):

    """
        Result protocol class.
    """

    @property
    @abc.abstractmethod
    def is_success(self) -> bool:

        """
            Returns True if result is a success object, otherwise False.
        """

    @property
    @abc.abstractmethod
    def is_failure(self) -> bool:

        """
            Returns True if result is a failure object, otherwise False.
        """


class SuccessObject(Result[ValueType, Any], Protocol[ValueType]):

    """
        Success object protocol class.
    """

    @property
    @abc.abstractmethod
    def value(self) -> ValueType:

        """
            Returns value wrapped by success object.
        """


class FailureObject(Result[Any, ErrorType], Protocol[ErrorType]):

    """
        Failure object protocol class.
    """

    @property
    @abc.abstractmethod
    def error(self) -> ErrorType:

        """
            Returns error wrapped by failure object.
        """


def success(value: Union[ValueType, SuccessObject[ValueType]], /) -> SuccessObject[ValueType]:

    """
        Returns value wrapped in success object.
        If value is already a success object, returns it.

        :param value: any object
    """

    if isinstance(value, Success):
        return value

    return Success(value)


def unwrap_success(result: Result[ValueType, ErrorType]) -> ValueType:

    """
        Unwraps value from given success object.

        :param result: success object
    """

    return Success.get_value(result)


def failure(error: Union[ErrorType, FailureObject[ErrorType]], /) -> FailureObject[ErrorType]:

    """
        Returns error wrapped in failure object.
        If error is already a failure object, returns it.

        :param error: exception object
    """

    if isinstance(error, Failure):
        return error

    return Failure(error)


def unwrap_failure(result: Result[ValueType, ErrorType]) -> ErrorType:

    """
        Unwraps error from given failure object.

        :param result: failure object
    """

    return Failure.get_error(result)
