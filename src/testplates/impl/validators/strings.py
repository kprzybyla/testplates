__all__ = ["StringValidator", "BytesValidator"]

from typing import Any, TypeVar, Union, Pattern as Regex, Optional, Final

import testplates

from testplates.impl.base import Result, Success, Failure
from testplates.impl.base import fits_minimum_length, fits_maximum_length, Limit, UnlimitedType
from testplates.impl.base import TestplatesError

from .type import TypeValidator
from .exceptions import (
    InvalidMinimumLengthError,
    InvalidMaximumLengthError,
    InvalidFormatError,
)

T = TypeVar("T", str, bytes)

AnyString = Union[str, bytes]
Boundary = Union[Limit, UnlimitedType]

string_type_validator: Final = TypeValidator((str,))
bytes_type_validator: Final = TypeValidator((bytes,))


class StringValidator:

    __slots__ = ("minimum", "maximum", "regex")

    def __init__(self, minimum: Boundary, maximum: Boundary, regex: Optional[Regex[str]]) -> None:
        self.minimum = minimum
        self.maximum = maximum
        self.regex = regex

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{type(self).__name__}()"

    # noinspection PyTypeChecker
    def __call__(self, data: Any) -> Result[None, TestplatesError]:
        if (error := string_type_validator(data)).is_failure:
            return Failure.from_result(error)

        if (error := validate_length(data, self.minimum, self.maximum)).is_failure:
            return Failure.from_result(error)

        if (error := validate_regex(data, self.regex)).is_failure:
            return Failure.from_result(error)

        return Success(None)


class BytesValidator:

    __slots__ = ("minimum", "maximum", "regex")

    def __init__(
        self, minimum: Boundary, maximum: Boundary, regex: Optional[Regex[bytes]]
    ) -> None:
        self.minimum = minimum
        self.maximum = maximum
        self.regex = regex

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"

    # noinspection PyTypeChecker
    def __call__(self, data: Any) -> Result[None, TestplatesError]:
        if (error := bytes_type_validator(data)).is_failure:
            return Failure.from_result(error)

        if (error := validate_length(data, self.minimum, self.maximum)).is_failure:
            return Failure.from_result(error)

        if (error := validate_regex(data, self.regex)).is_failure:
            return Failure.from_result(error)

        return Success(None)


# noinspection PyTypeChecker
def validate_length(
    data: AnyString, minimum: Boundary, maximum: Boundary, /
) -> Result[None, TestplatesError]:
    if not fits_minimum_length(data, minimum):
        return Failure(InvalidMinimumLengthError(data, minimum))

    if not fits_maximum_length(data, maximum):
        return Failure(InvalidMaximumLengthError(data, maximum))

    return Success(None)


# noinspection PyTypeChecker
def validate_regex(data: T, regex: Optional[Regex[T]], /) -> Result[None, TestplatesError]:
    if regex is not None:
        if not regex.match(data):
            return Failure(InvalidFormatError(data, regex))

    return Success(None)
