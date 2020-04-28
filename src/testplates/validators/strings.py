__all__ = ["any_string_validator", "string_validator", "bytes_validator"]

import re

from typing import overload, TypeVar, Callable, Optional, Final

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

validate_any_string_type: Final = type_validator(allowed_types=(str, bytes))
validate_string_type: Final = type_validator(allowed_types=str)
validate_bytes_type: Final = type_validator(allowed_types=bytes)


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
    if length is not None and (minimum_length is not None or maximum_length is not None):
        raise ...

    maximum, minimum = get_length_boundaries(
        inclusive_minimum=minimum_length, inclusive_maximum=maximum_length
    )

    regex = re.compile(pattern) if pattern is not None else None

    def validate(data: _T) -> Optional[Exception]:
        if (error := validate_any_string_type(data)) is not None:
            return error  # type: ignore

        if length is not None and len(data) != length:
            return InvalidLengthError(data, length)

        if minimum.fits(len(data)):
            return InvalidMinimumLengthError(data, minimum_length)

        if maximum.fits(len(data)):
            return InvalidMaximumLengthError(data, maximum_length)

        if regex is not None:
            if not isinstance(regex.pattern, type(data)):
                return InvalidPatternTypeError(data, regex)

            if not regex.match(data):
                return InvalidFormatError(data, regex)

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


# noinspection PyArgumentList
def string_validator(
    *,
    length: Optional[int] = None,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[str] = None,
) -> Callable[[str], Optional[Exception]]:
    validate_string: Callable[[str], Optional[Exception]] = any_string_validator(
        length=length,
        minimum_length=minimum_length,
        maximum_length=maximum_length,
        pattern=pattern,
    )  # type: ignore

    def validate(data: str) -> Optional[Exception]:
        if (error := validate_string_type(data)) is not None:
            return error

        return validate_string(data)

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


# noinspection PyArgumentList
def bytes_validator(
    *,
    length: Optional[int] = None,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[bytes] = None,
) -> Callable[[bytes], Optional[Exception]]:
    validate_bytes: Callable[[bytes], Optional[Exception]] = any_string_validator(
        length=length,
        minimum_length=minimum_length,
        maximum_length=maximum_length,
        pattern=pattern,
    )  # type: ignore

    def validate(data: bytes) -> Optional[Exception]:
        if (error := validate_bytes_type(data)) is not None:
            return error

        return validate_bytes(data)

    return validate
