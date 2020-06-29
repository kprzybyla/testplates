from __future__ import annotations

__all__ = ["Failure"]

from typing import Any, TypeVar, NoReturn

from .result import Result

_T = TypeVar("_T")


class Failure(Result[Any]):

    __slots__ = ()

    def __init__(self, error: Exception) -> None:
        super().__init__(None, error)

    # TODO(kprzybyla): Below method 'from_failure' is a workaround for mypy
    #                  that forces correct type hint using assert isinstance

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
