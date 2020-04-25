__all__ = ["any_string_validator", "string_validator", "bytes_validator"]

import re

from typing import TypeVar, Callable, Optional

from .type import type_validator
from .exceptions import (
    InvalidLengthError,
    InvalidMinimumLengthError,
    InvalidMaximumLengthError,
    InvalidPatternTypeError,
    InvalidFormatError,
)

_T = TypeVar("_T", str, bytes)

validate_any_string_type = type_validator(allowed_types=(str, bytes))
validate_string_type = type_validator(allowed_types=str)
validate_bytes_type = type_validator(allowed_types=bytes)


def any_string_validator(
    *,
    validate_type: Callable[[_T], Optional[Exception]] = validate_any_string_type,
    length: Optional[int] = None,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[_T] = None,
) -> Callable[[_T], Optional[Exception]]:
    # TODO(kprzybyla): Add validation or arguments here

    pattern = re.compile(pattern)

    def validate(data: _T) -> Optional[Exception]:
        if (error := validate_type(data)) is not None:
            return error

        if length is not None and len(data) != length:
            return InvalidLengthError(data, length)

        if minimum_length is not None and len(data) < minimum_length:
            return InvalidMinimumLengthError(data, minimum_length)

        if maximum_length is not None and len(data) > maximum_length:
            return InvalidMaximumLengthError(data, maximum_length)

        if pattern is not None and not isinstance(pattern.pattern, type(data)):
            return InvalidPatternTypeError(data, pattern)

        if pattern is not None and not pattern.match(data):
            return InvalidFormatError(data, pattern)

    return validate


def string_validator(
    *,
    length: Optional[int] = None,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[str] = None,
) -> Callable[[str], Optional[Exception]]:
    validate_string = any_string_validator(
        validate_type=validate_string_type,
        length=length,
        minimum_length=minimum_length,
        maximum_length=maximum_length,
        pattern=pattern,
    )

    def validate(data: str) -> Optional[Exception]:
        return validate_string(data)

    return validate


def bytes_validator(
    *,
    length: Optional[int] = None,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[bytes] = None,
) -> Callable[[bytes], Optional[Exception]]:
    validate_bytes = any_string_validator(
        validate_type=validate_bytes_type,
        length=length,
        minimum_length=minimum_length,
        maximum_length=maximum_length,
        pattern=pattern,
    )

    def validate(data: bytes) -> Optional[Exception]:
        return validate_bytes(data)

    return validate
