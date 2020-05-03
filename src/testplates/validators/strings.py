__all__ = ["any_string_validator", "string_validator", "bytes_validator"]

import re

from typing import overload, TypeVar, Union, Pattern as Regex, Callable, Optional, Final

from testplates.abc import Boundary
from testplates.boundaries import get_length_boundaries

from .type import type_validator
from .exceptions import (
    InvalidLengthError,
    InvalidMinimumLengthError,
    InvalidMaximumLengthError,
    InvalidPatternTypeError,
    InvalidFormatError,
)

_T = TypeVar("_T", str, bytes)

AnyString = Union[str, bytes]

validate_any_string_type: Final = type_validator(allowed_types=(str, bytes))
validate_string_type: Final = type_validator(allowed_types=str)
validate_bytes_type: Final = type_validator(allowed_types=bytes)


def get_regex(pattern: Optional[_T]) -> Optional[Regex[_T]]:
    return re.compile(pattern) if pattern is not None else None


@overload
def any_string_validator(
    *, length: Optional[int] = None, pattern: Optional[_T] = None
) -> Callable[[_T], Optional[Exception]]:
    ...


@overload
def any_string_validator(
    *,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[_T] = None,
) -> Callable[[_T], Optional[Exception]]:
    ...


def any_string_validator(
    *,
    length: Optional[int] = None,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[_T] = None,
) -> Callable[[_T], Optional[Exception]]:
    maximum, minimum = get_length_boundaries(length, minimum_length, maximum_length)
    regex = get_regex(pattern)

    def validate(data: _T) -> Optional[Exception]:
        if (error := validate_any_string_type(data)) is not None:
            return error

        if (error := validate_any_string_length(data, length, minimum, maximum)) is not None:
            return error

        if (error := validate_any_string_regex(data, regex)) is not None:
            return error

        return None

    return validate


@overload
def string_validator(
    *, length: Optional[int] = None, pattern: Optional[str] = None
) -> Callable[[str], Optional[Exception]]:
    ...


@overload
def string_validator(
    *,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[str] = None,
) -> Callable[[str], Optional[Exception]]:
    ...


def string_validator(
    *,
    length: Optional[int] = None,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[str] = None,
) -> Callable[[str], Optional[Exception]]:
    maximum, minimum = get_length_boundaries(length, minimum_length, maximum_length)
    regex = get_regex(pattern)

    def validate(data: str) -> Optional[Exception]:
        if (error := validate_string_type(data)) is not None:
            return error

        if (error := validate_any_string_length(data, length, minimum, maximum)) is not None:
            return error

        if (error := validate_any_string_regex(data, regex)) is not None:
            return error

        return None

    return validate


@overload
def bytes_validator(
    *, length: Optional[int] = None, pattern: Optional[bytes] = None
) -> Callable[[bytes], Optional[Exception]]:
    ...


@overload
def bytes_validator(
    *,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[bytes] = None,
) -> Callable[[bytes], Optional[Exception]]:
    ...


def bytes_validator(
    *,
    length: Optional[int] = None,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[bytes] = None,
) -> Callable[[bytes], Optional[Exception]]:
    maximum, minimum = get_length_boundaries(length, minimum_length, maximum_length)
    regex = get_regex(pattern)

    def validate(data: bytes) -> Optional[Exception]:
        if (error := validate_bytes_type(data)) is not None:
            return error

        if (error := validate_any_string_length(data, length, minimum, maximum)) is not None:
            return error

        if (error := validate_any_string_regex(data, regex)) is not None:
            return error

        return None

    return validate


def validate_any_string_length(
    data: AnyString, length: Optional[int], minimum: Boundary[int], maximum: Boundary[int], /
) -> Optional[Exception]:
    if length is not None and len(data) != length:
        return InvalidLengthError(data, length)

    if minimum.fits(len(data)):
        return InvalidMinimumLengthError(data, minimum)

    if maximum.fits(len(data)):
        return InvalidMaximumLengthError(data, maximum)

    return None


def validate_any_string_regex(data: _T, regex: Optional[Regex[_T]], /) -> Optional[Exception]:
    if regex is not None:
        if not isinstance(regex.pattern, type(data)):
            return InvalidPatternTypeError(data, regex)

        if not regex.match(data):
            return InvalidFormatError(data, regex)

    return None
