from __future__ import annotations

__all__ = ["Failure"]

from typing import Any, TypeVar, Generic

from .result import Result

_E = TypeVar("_E", bound=Exception)


class Failure(Result[Any, _E], Generic[_E]):

    __slots__ = ()

    def __init__(self, error: _E) -> None:
        super().__init__(None, error)

    @classmethod
    def from_result(cls, result: Result[Any, _E]) -> Failure[_E]:

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
    def error(self) -> _E:
        error = self._error

        assert error is not None
        return error
