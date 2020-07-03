from __future__ import annotations

__all__ = ["Failure"]

from typing import Any, TypeVar, Generic

from .result import Result

ErrorType = TypeVar("ErrorType", bound=Exception)


class Failure(Result[Any, ErrorType], Generic[ErrorType]):

    __slots__ = ()

    def __init__(self, error: ErrorType) -> None:
        super().__init__(None, error)

    @classmethod
    def from_result(cls, result: Result[Any, ErrorType]) -> Failure[ErrorType]:

        """
            Returns failure from result.

            :param result: result from which failure is created
        """

        assert isinstance(result, Failure)
        return result

    @property
    def value(self) -> None:
        value = self._value

        assert value is None
        return value

    @property
    def error(self) -> ErrorType:
        error = self._error

        assert error is not None
        return error
