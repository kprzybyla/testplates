__all__ = ["String", "ByteString", "BitString", "HexString"]

import re

from typing import TypeVar, Generic, Optional, Final

from .base_validator import BaseValidator
from .exceptions import (
    InvalidTypeError,
    InvalidLengthError,
    InvalidMinimumLengthError,
    InvalidMaximumLengthError,
    InvalidPatternTypeError,
    InvalidFormatError,
)

_T = TypeVar("_T", str, bytes)

BITSTRING_PATTERN: Final[str] = re.compile("[01]*")
HEXSTRING_PATTERN: Final[str] = re.compile("(?:0x)?[0-9a-fA-F]*")


class BaseString(BaseValidator[_T], Generic[_T]):

    __slots__ = ("_length", "_minimum_length", "_maximum_length", "_pattern")

    def __init__(
        self,
        length: Optional[int] = None,
        minimum_length: Optional[int] = None,
        maximum_length: Optional[int] = None,
        pattern: Optional[_T] = None,
    ) -> None:
        self._length = length
        self._minimum_length = minimum_length
        self._maximum_length = maximum_length
        self._pattern = re.compile(pattern)

        # TODO(kprzybyla): Add validation or arguments here

    def validate(self, data: _T) -> None:
        if not isinstance(data, (str, bytes)):
            raise InvalidTypeError(data, (str, bytes))

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
    pass


class ByteString(BaseString[bytes]):
    pass


class BitString(String):

    __slots__ = ()

    def __init__(
        self,
        length: Optional[int] = None,
        minimum_length: Optional[int] = None,
        maximum_length: Optional[int] = None,
    ):
        super().__init__(
            length=length,
            minimum_length=minimum_length,
            maximum_length=maximum_length,
            pattern=BITSTRING_PATTERN,
        )


class HexString(String):

    __slots__ = ()

    def __init__(
        self,
        length: Optional[int] = None,
        minimum_length: Optional[int] = None,
        maximum_length: Optional[int] = None,
    ):
        super().__init__(
            length=length,
            minimum_length=minimum_length,
            maximum_length=maximum_length,
            pattern=HEXSTRING_PATTERN,
        )
