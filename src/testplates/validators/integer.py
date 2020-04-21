__all__ = ["Integer"]

from typing import Optional

from .base_validator import BaseValidator
from .exceptions import InvalidTypeError, InvalidMinimumValueError, InvalidMaximumValueError


class Integer(BaseValidator[int]):

    __slots__ = ("_minimum_value", "_maximum_value")

    def __init__(
        self, minimum_value: Optional[int] = None, maximum_value: Optional[int] = None
    ) -> None:
        self._minimum_value = minimum_value
        self._maximum_value = maximum_value

        # TODO(kprzybyla): Add validation or arguments here

    def validate(self, data: int) -> None:
        if not isinstance(data, int):
            raise InvalidTypeError(data, int)

        if isinstance(data, bool):
            raise InvalidTypeError(data, int)

        if self._minimum_value is not None and data < self._minimum_value:
            raise InvalidMinimumValueError(data, self._minimum_value)

        if self._maximum_value is not None and data > self._maximum_value:
            raise InvalidMaximumValueError(data, self._maximum_value)
