__all__ = ["String", "ByteString"]

import re

from typing import Type, TypeVar, Generic, Optional

from .base_validator import BaseValidator
from .exceptions import (
    InvalidLengthError,
    InvalidMinimumLengthError,
    InvalidMaximumLengthError,
    InvalidPatternTypeError,
    InvalidFormatError,
)

_T = TypeVar("_T", str, bytes)


class BaseString(BaseValidator[_T], Generic[_T]):

    __slots__ = ("_length", "_minimum_length", "_maximum_length", "_pattern")

    def __init__(
        self,
        *,
        length: Optional[int] = None,
        minimum_length: Optional[int] = None,
        maximum_length: Optional[int] = None,
        pattern: Optional[_T] = None,
    ) -> None:
        # TODO(kprzybyla): Add validation or arguments here

        self._length = length
        self._minimum_length = minimum_length
        self._maximum_length = maximum_length
        self._pattern = re.compile(pattern)

    @property
    def allowed_types(self) -> Type[_T]:
        return str, bytes

    def validate(self, data: _T) -> None:
        super().validate(data)

        if self._length is not None and len(data) != self._length:
            raise InvalidLengthError(data, self._length)

        if self._minimum_length is not None and len(data) < self._minimum_length:
            raise InvalidMinimumLengthError(data, self._minimum_length)

        if self._maximum_length is not None and len(data) > self._maximum_length:
            raise InvalidMaximumLengthError(data, self._maximum_length)

        if self._pattern is not None and not isinstance(self._pattern.pattern, type(data)):
            raise InvalidPatternTypeError(data, self._pattern)

        if self._pattern is not None and not self._pattern.match(data):
            raise InvalidFormatError(data, self._pattern)


class String(BaseString[str]):

    __slots__ = ()

    @property
    def allowed_types(self) -> Type[str]:
        return str


class ByteString(BaseString[bytes]):

    __slots__ = ()

    @property
    def allowed_types(self) -> Type[bytes]:
        return bytes
