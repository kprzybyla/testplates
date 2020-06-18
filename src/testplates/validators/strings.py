__all__ = ["any_string_validator", "string_validator", "bytes_validator"]

import re

from typing import overload, TypeVar, Union, Pattern as Regex, Callable, Optional, Final

from testplates.result import Result, Success, Failure
from testplates.boundaries import get_length_boundaries, Boundary

from .type import type_validator
from .utils import Validator
from .exceptions import (
    InvalidLengthError,
    InvalidMinimumLengthError,
    InvalidMaximumLengthError,
    InvalidPatternTypeError,
    InvalidFormatError,
)

_T = TypeVar("_T", str, bytes)

AnyString = Union[str, bytes]

validate_any_string_type: Final = type_validator(allowed_types=(str, bytes)).value
validate_string_type: Final = type_validator(allowed_types=str).value
validate_bytes_type: Final = type_validator(allowed_types=bytes).value


def get_regex(pattern: Optional[_T]) -> Optional[Regex[_T]]:
    return re.compile(pattern) if pattern is not None else None


@overload
def any_string_validator(
    *, length: Optional[int] = None, pattern: Optional[_T] = None
) -> Result[Validator[_T]]:
    ...


@overload
def any_string_validator(
    *,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[_T] = None,
) -> Result[Validator[_T]]:
    ...


def any_string_validator(
    *,
    length: Optional[int] = None,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[_T] = None,
) -> Result[Validator[_T]]:
    result = get_length_boundaries(minimum_value=minimum_length, maximum_value=maximum_length)

    if result.is_error:
        return Failure.from_failure(result)

    minimum, maximum = result.value
    regex = get_regex(pattern)

    def validate(data: _T) -> Result[None]:
        if (error := validate_any_string_type(data)) is not None:
            return Failure.from_failure(error)

        if (error := validate_any_string_length(data, length, minimum, maximum)) is not None:
            return Failure.from_failure(error)

        if (error := validate_any_string_regex(data, regex)) is not None:
            return Failure.from_failure(error)

        return Success(None)

    return Success(validate)


@overload
def string_validator(
    *, length: Optional[int] = None, pattern: Optional[str] = None
) -> Result[Validator[str]]:
    ...


@overload
def string_validator(
    *,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[str] = None,
) -> Result[Validator[str]]:
    ...


def string_validator(
    *,
    length: Optional[int] = None,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[str] = None,
) -> Result[Validator[str]]:
    result = get_length_boundaries(minimum_value=minimum_length, maximum_value=maximum_length)

    if result.is_error:
        return Failure.from_failure(result)

    minimum, maximum = result.value
    regex = get_regex(pattern)

    def validate(data: str) -> Result[None]:
        if (error := validate_string_type(data)) is not None:
            return Failure.from_failure(error)

        if (error := validate_any_string_length(data, length, minimum, maximum)) is not None:
            return Failure.from_failure(error)

        if (error := validate_any_string_regex(data, regex)) is not None:
            return Failure.from_failure(error)

        return Success(None)

    return Success(validate)


@overload
def bytes_validator(
    *, length: Optional[int] = None, pattern: Optional[bytes] = None
) -> Result[Validator[bytes]]:
    ...


@overload
def bytes_validator(
    *,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[bytes] = None,
) -> Result[Validator[bytes]]:
    ...


def bytes_validator(
    *,
    length: Optional[int] = None,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[bytes] = None,
) -> Result[Callable[[bytes], Result[None]]]:
    result = get_length_boundaries(minimum_value=minimum_length, maximum_value=maximum_length)

    if result.is_error:
        return Failure.from_failure(result)

    minimum, maximum = result.value
    regex = get_regex(pattern)

    def validate(data: bytes) -> Result[None]:
        if (error := validate_bytes_type(data)) is not None:
            return Failure.from_failure(error)

        if (error := validate_any_string_length(data, length, minimum, maximum)) is not None:
            return Failure.from_failure(error)

        if (error := validate_any_string_regex(data, regex)) is not None:
            return Failure.from_failure(error)

        return Success(None)

    return Success(validate)


def validate_any_string_length(
    data: AnyString, length: Optional[int], minimum: Boundary[int], maximum: Boundary[int], /
) -> Result[None]:
    if length is not None and len(data) != length:
        return Failure(InvalidLengthError(data, length))

    if minimum.fits(len(data)):
        return Failure(InvalidMinimumLengthError(data, minimum))

    if maximum.fits(len(data)):
        return Failure(InvalidMaximumLengthError(data, maximum))

    return Success(None)


def validate_any_string_regex(data: _T, regex: Optional[Regex[_T]], /) -> Result[None]:
    if regex is not None:
        if not isinstance(regex.pattern, type(data)):
            return Failure(InvalidPatternTypeError(data, regex))

        if not regex.match(data):
            return Failure(InvalidFormatError(data, regex))

    return Success(None)
