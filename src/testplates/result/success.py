__all__ = ["Success"]

from typing import TypeVar, Generic, NoReturn

from .result import Result

_T = TypeVar("_T")


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
