__all__ = ["any_string_validator", "string_validator", "bytes_validator"]

import re

from typing import overload, Any, TypeVar, Generic, Union, Pattern as Regex, Optional, Final

from testplates.result import Result, Success, Failure
from testplates.boundaries import (
    get_length_boundaries,
    fits_minimum_length,
    fits_maximum_length,
    Boundary,
)

from .type import type_validator
from .utils import Validator
from .exceptions import (
    ValidationError,
    InvalidLengthError,
    InvalidMinimumLengthError,
    InvalidMaximumLengthError,
    InvalidPatternTypeError,
    InvalidFormatError,
)

_T = TypeVar("_T", str, bytes)

AnyString = Union[str, bytes]

any_string_type_validator: Final = Success.get_value(type_validator(str, bytes))
string_type_validator: Final = Success.get_value(type_validator(str))
bytes_type_validator: Final = Success.get_value(type_validator(bytes))


class AnyStringValidator(Generic[_T]):

    __slots__ = ("length", "minimum", "maximum", "regex")

    def __init__(
        self,
        length: Optional[int],
        minimum: Boundary,
        maximum: Boundary,
        regex: Optional[Regex[_T]],
    ) -> None:
        self.length = length
        self.minimum = minimum
        self.maximum = maximum
        self.regex = regex

    def __repr__(self) -> str:
        return f"{any_string_validator.__name__}()"

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
        self.type_validator = type_validator
        self.length = length
        self.minimum = minimum
        self.maximum = maximum
        self.regex = regex

    def __repr__(self) -> str:
        return f"{string_validator.__name__}()"

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
        return f"{bytes_validator.__name__}()"

    # noinspection PyTypeChecker
    def __call__(self, data: Any) -> Result[None, ValidationError]:
        if (error := bytes_type_validator(data)) is not None:
            return Failure.from_result(error)

        if (error := validate_length(data, self.length, self.minimum, self.maximum)) is not None:
            return Failure.from_result(error)

        if (error := validate_regex(data, self.regex)) is not None:
            return Failure.from_result(error)

        return Success(None)


@overload
def any_string_validator(
    *, length: Optional[int] = None, pattern: Optional[_T] = None
) -> Result[Validator, ValidationError]:
    ...


@overload
def any_string_validator(
    *,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[_T] = None,
) -> Result[Validator, ValidationError]:
    ...


# noinspection PyTypeChecker
def any_string_validator(
    *,
    length: Optional[int] = None,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[_T] = None,
) -> Result[Validator, ValidationError]:
    result = get_length_boundaries(
        inclusive_minimum=minimum_length, inclusive_maximum=maximum_length
    )

    if result.is_failure:
        return Failure.from_result(result)

    minimum, maximum = Success.get_value(result)
    regex = get_regex(pattern)

    return Success(AnyStringValidator(length, minimum, maximum, regex))


@overload
def string_validator(
    *, length: Optional[int] = None, pattern: Optional[str] = None
) -> Result[Validator, ValidationError]:
    ...


@overload
def string_validator(
    *,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[str] = None,
) -> Result[Validator, ValidationError]:
    ...


# noinspection PyTypeChecker
def string_validator(
    *,
    length: Optional[int] = None,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[str] = None,
) -> Result[Validator, ValidationError]:
    result = get_length_boundaries(
        inclusive_minimum=minimum_length, inclusive_maximum=maximum_length
    )

    if result.is_failure:
        return Failure.from_result(result)

    minimum, maximum = Success.get_value(result)
    regex = get_regex(pattern)

    return Success(StringValidator(length, minimum, maximum, regex))


@overload
def bytes_validator(
    *, length: Optional[int] = None, pattern: Optional[bytes] = None
) -> Result[Validator, ValidationError]:
    ...


@overload
def bytes_validator(
    *,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[bytes] = None,
) -> Result[Validator, ValidationError]:
    ...


# noinspection PyTypeChecker
def bytes_validator(
    *,
    length: Optional[int] = None,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[bytes] = None,
) -> Result[Validator, ValidationError]:
    result = get_length_boundaries(
        inclusive_minimum=minimum_length, inclusive_maximum=maximum_length
    )

    if result.is_failure:
        return Failure.from_result(result)

    minimum, maximum = Success.get_value(result)
    regex = get_regex(pattern)

    return Success(BytesValidator(length, minimum, maximum, regex))


def get_regex(pattern: Optional[_T]) -> Optional[Regex[_T]]:
    return re.compile(pattern) if pattern is not None else None


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
def validate_regex(data: _T, regex: Optional[Regex[_T]], /) -> Result[None, ValidationError]:
    if regex is not None:
        if not isinstance(regex.pattern, type(data)):
            return Failure(InvalidPatternTypeError(data, regex))

        if not regex.match(data):
            return Failure(InvalidFormatError(data, regex))

    return Success(None)
