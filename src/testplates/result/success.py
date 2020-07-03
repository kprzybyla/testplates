from __future__ import annotations

__all__ = ["Success"]

from typing import Any, TypeVar, Generic, NoReturn

import testplates

from .result import Result

ValueType = TypeVar("ValueType")


class Success(Result[ValueType, Any], Generic[ValueType]):

    __slots__ = ("_value",)

    def __init__(self, value: ValueType) -> None:
        super().__init__()

        self._value = value

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{type(self).__name__}({self.value})"

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
        return self._value

    @property
    def error(self) -> NoReturn:
        raise NotImplementedError()
