__all__ = ["Result"]

from typing import TypeVar, Generic, Optional

from testplates import result

_T = TypeVar("_T")


class Result(Generic[_T]):

    __slots__ = ("_value", "_error")

    def __init__(self, value: Optional[_T], error: Optional[Exception]) -> None:
        self._value = value
        self._error = error

    @property
    def is_value(self) -> bool:
        return isinstance(self, result.Success)

    @property
    def is_error(self) -> bool:
        return isinstance(self, result.Failure)

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
