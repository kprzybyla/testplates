from __future__ import annotations

__all__ = ["Success"]

from typing import Any, TypeVar, Generic

from .result import Result

_T = TypeVar("_T")


class Success(Generic[_T], Result[_T, Any]):

    __slots__ = ()

    def __init__(self, value: _T) -> None:
        super().__init__(value, None)

    @classmethod
    def from_result(cls, result: Result[_T, Any]) -> Success[_T]:
        assert isinstance(result, Success)
        return result

    @property
    def value(self) -> _T:
        value = self._value

        assert value is not None
        return value

    @property
    def error(self) -> None:
        error = self._error

        assert error is None
        return error
