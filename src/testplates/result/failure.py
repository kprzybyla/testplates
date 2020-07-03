from __future__ import annotations

__all__ = ["Failure"]

from typing import Any, TypeVar, Generic

import testplates

from .result import Result

ErrorType = TypeVar("ErrorType", bound=Exception)


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

    @property
    def is_success(self) -> bool:
        return False

    @property
    def is_failure(self) -> bool:
        return True

    @property
    def error(self) -> ErrorType:
        return self._error
