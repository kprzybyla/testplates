from __future__ import annotations

__all__ = ["Success"]

from typing import Any, TypeVar, Generic

import testplates

from .result import Result

ValueType = TypeVar("ValueType")


class Success(Result[ValueType, Any], Generic[ValueType]):

    __slots__ = ("_value",)

    def __init__(self, value: ValueType) -> None:
        self._value = value

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{type(self).__name__}({self.value})"

    @classmethod
    def from_result(cls, result: Result[ValueType, Any]) -> Success[ValueType]:

        """
            Returns success from result.

            :param result: result from which success is created
        """

        assert isinstance(result, Success), result
        return result

    @classmethod
    def get_value(cls, result: Result[ValueType, Any]) -> ValueType:

        """
            Returns value from result.

            :param result: result from which value is extracted
        """

        return cls.from_result(result).value

    @property
    def is_success(self) -> bool:
        return True

    @property
    def is_failure(self) -> bool:
        return False

    @property
    def value(self) -> ValueType:
        return self._value
