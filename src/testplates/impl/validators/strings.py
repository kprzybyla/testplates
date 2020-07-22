__all__ = ["AnyStringValidator", "StringValidator", "BytesValidator"]

from typing import Any, TypeVar, Generic, Union, Pattern as Regex, Optional, Final

from testplates.impl.base import Result, Success, Failure
from testplates.impl.base import (
    fits_minimum_length,
    fits_maximum_length,
    Limit,
    UnlimitedType,
    InvalidLengthError,
)

from .type import TypeValidator
from .exceptions import (
    ValidationError,
    # TODO(kprzybyla)
    # InvalidLengthError,
    InvalidMinimumLengthError,
    InvalidMaximumLengthError,
    InvalidPatternTypeError,
    InvalidFormatError,
)

T = TypeVar("T", str, bytes)

AnyString = Union[str, bytes]
Boundary = Union[Limit, UnlimitedType]

any_string_type_validator: Final = TypeValidator((str, bytes))
string_type_validator: Final = TypeValidator((str,))
bytes_type_validator: Final = TypeValidator((bytes,))


class AnyStringValidator(Generic[T]):

    __slots__ = ("length", "minimum", "maximum", "regex")

    def __init__(
        self,
        length: Optional[int],
        minimum: Boundary,
        maximum: Boundary,
        regex: Optional[Regex[T]],
    ) -> None:
        self.length = length
        self.minimum = minimum
        self.maximum = maximum
        self.regex = regex

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"

    # noinspection PyTypeChecker
    def __call__(self, data: Any) -> Result[None, ValidationError]:
        if (error := any_string_type_validator(data)) is not None:
            return Failure.from_result(error)

        if (error := validate_length(data, self.length, self.minimum, self.maximum)) is not None:
            return Failure.from_result(error)

        if (error := validate_regex(data, self.regex)) is not None:
            return Failure.from_result(error)

        return Success(None)


class StringValidator:

    __slots__ = ("type_validator", "length", "minimum", "maximum", "regex")

    def __init__(
        self,
        length: Optional[int],
        minimum: Boundary,
        maximum: Boundary,
        regex: Optional[Regex[str]],
    ) -> None:
        self.length = length
        self.minimum = minimum
        self.maximum = maximum
        self.regex = regex

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"

    # noinspection PyTypeChecker
    def __call__(self, data: Any) -> Result[None, ValidationError]:
        if (error := string_type_validator(data)) is not None:
            return Failure.from_result(error)

        if (error := validate_length(data, self.length, self.minimum, self.maximum)) is not None:
            return Failure.from_result(error)

        if (error := validate_regex(data, self.regex)) is not None:
            return Failure.from_result(error)

        return Success(None)


class BytesValidator:

    __slots__ = ("length", "minimum", "maximum", "regex")

    def __init__(
        self,
        length: Optional[int],
        minimum: Boundary,
        maximum: Boundary,
        regex: Optional[Regex[bytes]],
    ) -> None:
        self.length = length
        self.minimum = minimum
        self.maximum = maximum
        self.regex = regex

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"

    # noinspection PyTypeChecker
    def __call__(self, data: Any) -> Result[None, ValidationError]:
        if (error := bytes_type_validator(data)) is not None:
            return Failure.from_result(error)

        if (error := validate_length(data, self.length, self.minimum, self.maximum)) is not None:
            return Failure.from_result(error)

        if (error := validate_regex(data, self.regex)) is not None:
            return Failure.from_result(error)

        return Success(None)


# noinspection PyTypeChecker
def validate_length(
    data: AnyString, length: Optional[int], minimum: Boundary, maximum: Boundary, /
) -> Result[None, ValidationError]:
    if length is not None and len(data) != length:
        return Failure(InvalidLengthError(data, length))

    if fits_minimum_length(data, minimum):
        return Failure(InvalidMinimumLengthError(data, minimum))

    if fits_maximum_length(data, maximum):
        return Failure(InvalidMaximumLengthError(data, maximum))

    return Success(None)


# noinspection PyTypeChecker
def validate_regex(data: T, regex: Optional[Regex[T]], /) -> Result[None, ValidationError]:
    if regex is not None:
        if not isinstance(regex.pattern, type(data)):
            return Failure(InvalidPatternTypeError(data, regex))

        if not regex.match(data):
            return Failure(InvalidFormatError(data, regex))

    return Success(None)
