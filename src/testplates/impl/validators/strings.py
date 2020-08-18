__all__ = ["StringValidator", "BytesValidator"]

from typing import Any, AnyStr, Union, Pattern, Optional, Final

from resultful import success, failure, Result

import testplates

from testplates.impl.base import fits_minimum_length, fits_maximum_length, Limit, UnlimitedType
from testplates.impl.base import TestplatesError

from .type import TypeValidator
from .exceptions import (
    InvalidMinimumSizeError,
    InvalidMaximumSizeError,
    InvalidFormatError,
)

Boundary = Union[Limit, UnlimitedType]

string_type_validator: Final = TypeValidator(str)
bytes_type_validator: Final = TypeValidator(bytes)


class StringValidator:

    __slots__ = ("minimum_length", "maximum_length", "pattern")

    def __init__(
        self,
        *,
        minimum_length: Boundary,
        maximum_length: Boundary,
        pattern: Optional[Pattern[str]],
    ) -> None:
        self.minimum_length = minimum_length
        self.maximum_length = maximum_length
        self.pattern = pattern

    def __repr__(self) -> str:
        return f"{testplates.__name__}.string_validator()"

    def __call__(self, data: Any, /) -> Result[None, TestplatesError]:
        if not (result := string_type_validator(data)):
            return failure(result)

        if not (result := validate_length(data, self.minimum_length, self.maximum_length)):
            return failure(result)

        if not (result := validate_pattern(data, self.pattern)):
            return failure(result)

        return success(None)


class BytesValidator:

    __slots__ = ("minimum_length", "maximum_length", "pattern")

    def __init__(
        self,
        *,
        minimum_length: Boundary,
        maximum_length: Boundary,
        pattern: Optional[Pattern[bytes]],
    ) -> None:
        self.minimum_length = minimum_length
        self.maximum_length = maximum_length
        self.pattern = pattern

    def __repr__(self) -> str:
        return f"{testplates.__name__}.bytes_validator()"

    def __call__(self, data: Any) -> Result[None, TestplatesError]:
        if not (result := bytes_type_validator(data)):
            return failure(result)

        if not (result := validate_length(data, self.minimum_length, self.maximum_length)):
            return failure(result)

        if not (result := validate_pattern(data, self.pattern)):
            return failure(result)

        return success(None)


def validate_length(
    data: AnyStr, minimum_length: Boundary, maximum_length: Boundary, /
) -> Result[None, TestplatesError]:
    if not fits_minimum_length(data, minimum_length):
        return failure(InvalidMinimumSizeError(data, minimum_length))

    if not fits_maximum_length(data, maximum_length):
        return failure(InvalidMaximumSizeError(data, maximum_length))

    return success(None)


def validate_pattern(
    data: AnyStr, pattern: Optional[Pattern[AnyStr]], /
) -> Result[None, TestplatesError]:
    if pattern is not None:
        if not pattern.match(data):
            return failure(InvalidFormatError(data, pattern))

    return success(None)
