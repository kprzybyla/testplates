__all__ = ["sequence_validator"]

import typing

from typing import TypeVar, Callable, Optional

from testplates.result import Result, Success, Failure
from testplates.boundaries import get_length_boundaries

from .type import type_validator
from .utils import validate_any, has_unique_items, Validator
from .exceptions import (
    ItemValidationError,
    InvalidMinimumSizeError,
    InvalidMaximumSizeError,
    UniquenessError,
)

_T = TypeVar("_T")

validate_sequence_type = type_validator(allowed_types=typing.Sequence).value

# TODO(kprzybyla): Add overloads for validators


def sequence_validator(
    validate_item: Callable[[_T], Optional[Exception]] = validate_any,
    /,
    *,
    size: Optional[int] = None,
    minimum_size: Optional[int] = None,
    maximum_size: Optional[int] = None,
    unique_items: bool = False,
) -> Result[Validator[typing.Sequence[_T]]]:
    result = get_length_boundaries(minimum_value=minimum_size, maximum_value=maximum_size)

    if result.is_error:
        return Failure.from_failure(result)

    minimum, maximum = result.value

    def validate(data: typing.Sequence[_T]) -> Result[None]:
        if (error := validate_sequence_type(data)) is not None:
            return Failure.from_failure(error)

        for item in data:
            if (error := validate_item(item)) is not None:
                return Failure(ItemValidationError(error))

        if size is not None and len(data) != size:
            return Failure(...)

        if not minimum.fits(len(data)):
            return Failure(InvalidMinimumSizeError(data, minimum))

        if not maximum.fits(len(data)):
            return Failure(InvalidMaximumSizeError(data, maximum))

        if unique_items and not has_unique_items(data):
            return Failure(UniquenessError(data))

        return Success(None)

    return Success(validate)
