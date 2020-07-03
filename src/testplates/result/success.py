from __future__ import annotations

__all__ = ["Success"]

from typing import Any, TypeVar, Generic

from .result import Result

ValueType = TypeVar("ValueType")


class Success(Result[ValueType, Any], Generic[ValueType]):

    __slots__ = ()

    def __init__(self, value: ValueType) -> None:
        super().__init__(value, None)

    @classmethod
    def from_result(cls, result: Result[ValueType, Any]) -> Success[ValueType]:

        """
            Returns success from result.

            :param result: result from which success is created
        """

        assert isinstance(result, Success)
        return result

    @property
    def value(self) -> ValueType:
        value = self._value

        assert value is not None
        return value

    @property
    def error(self) -> None:
        error = self._error

        assert error is None
        return error
