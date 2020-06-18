from __future__ import annotations

from typing import Any, TypeVar, Generic, NoReturn, Optional

_T = TypeVar("_T")


class Result(Generic[_T]):

    __slots__ = ("_value", "_error")

    def __init__(self, value: Optional[_T], error: Optional[Exception]) -> None:
        self._value = value
        self._error = error

    @property
    def is_value(self) -> bool:
        return isinstance(self, Success)

    @property
    def is_error(self) -> bool:
        return isinstance(self, Failure)

    @property
    def value(self) -> _T:
        value = self.value

        if value is None:
            raise TypeError(...)

        return value

    @property
    def error(self) -> Exception:
        error = self.error

        if error is None:
            raise TypeError(...)

        return error


class Success(Result[_T], Generic[_T]):

    __slots__ = ()

    def __init__(self, value: _T) -> None:
        super().__init__(value, None)

    @property
    def value(self) -> _T:
        return self._value

    @property
    def error(self) -> NoReturn:
        raise TypeError(...)


class Failure(Result[Any]):

    __slots__ = ()

    def __init__(self, error: Exception) -> None:
        super().__init__(None, error)

    # TODO(kprzybyla): This is a workaround for mypy

    @classmethod
    def from_failure(cls, failure: Result[Any]) -> Failure:
        assert isinstance(failure, Failure)
        return failure

    @property
    def value(self) -> NoReturn:
        raise TypeError(...)

    @property
    def error(self) -> Exception:
        return self._error
