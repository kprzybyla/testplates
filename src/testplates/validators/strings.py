__all__ = ["any_string_validator", "string_validator", "bytes_validator"]

import re

from typing import TypeVar, Callable, Optional, Final

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


def any_string_validator(
    *,
    length: Optional[int] = None,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[_T] = None,
) -> Callable[[_T], Optional[Exception]]:
    # TODO(kprzybyla): Add validation or arguments here

    regex = re.compile(pattern) if pattern is not None else None

    def validate(data: _T) -> Optional[Exception]:
        if (error := validate_any_string_type(data)) is not None:
            return error  # type: ignore

        if length is not None and len(data) != length:
            return InvalidLengthError(data, length)

        if minimum_length is not None and len(data) < minimum_length:
            return InvalidMinimumLengthError(data, minimum_length)

        if maximum_length is not None and len(data) > maximum_length:
            return InvalidMaximumLengthError(data, maximum_length)

        if regex is not None and not isinstance(regex.pattern, type(data)):
            return InvalidPatternTypeError(data, regex)

        if regex is not None and not regex.match(data):
            return InvalidFormatError(data, regex)

        return None

    return validate


def string_validator(
    *,
    length: Optional[int] = None,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    pattern: Optional[str] = None,
) -> Callable[[str], Optional[Exception]]:
    validate_string = any_string_validator(
        length=length,
        minimum_length=minimum_length,
        maximum_length=maximum_length,
        pattern=pattern,
    )

    def validate(data: str) -> Optional[Exception]:
        if (error := validate_string_type(data)) is not None:
            return error  # type: ignore

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
        length=length,
        minimum_length=minimum_length,
        maximum_length=maximum_length,
        pattern=pattern,
    )

    def validate(data: bytes) -> Optional[Exception]:
        if (error := validate_bytes_type(data)) is not None:
            return error  # type: ignore

        return validate_bytes(data)

    return validate
