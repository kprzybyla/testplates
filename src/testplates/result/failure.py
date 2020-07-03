from __future__ import annotations

__all__ = ["Failure"]

from typing import Any, TypeVar, Generic, NoReturn

import testplates

from .result import Result

ErrorType = TypeVar("ErrorType", bound=Exception)


class Failure(Result[Any, ErrorType], Generic[ErrorType]):

    __slots__ = ("_error",)

    def __init__(self, error: ErrorType) -> None:
        super().__init__()

        self._error = error

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{type(self).__name__}({self.error})"

    @classmethod
    def from_result(cls, result: Result[Any, ErrorType]) -> Failure[ErrorType]:

        """
            Returns failure from result.

            :param result: result from which failure is created
        """

        assert isinstance(result, Failure)
        return result

    @property
    def value(self) -> NoReturn:
        raise NotImplementedError()

    @property
    def error(self) -> ErrorType:
        return self._error
