__all__ = ["sequence_validator"]

import typing

from typing import TypeVar, Callable, Optional

from testplates.boundaries import get_minimum, get_maximum, check_length_boundaries

from .type import type_validator
from .utils import validate_any, has_unique_items, Result, Validator
from .exceptions import (
    ItemValidationError,
    InvalidMinimumSizeError,
    InvalidMaximumSizeError,
    UniquenessError,
)

_T = TypeVar("_T")

validate_sequence_type = type_validator(allowed_types=typing.Sequence)

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
    minimum = get_minimum(inclusive=minimum_size)

    if isinstance(minimum, Exception):
        return minimum

    maximum = get_maximum(inclusive=maximum_size)

    if isinstance(maximum, Exception):
        return maximum

    outcome = check_length_boundaries(minimum=minimum, maximum=maximum)

    if outcome is not None:
        return outcome

    def validate(data: typing.Sequence[_T]) -> Optional[Exception]:
        if (error := validate_sequence_type(data)) is not None:
            return error

        for item in data:
            if (error := validate_item(item)) is not None:
                return ItemValidationError(error)

        if not minimum.fits(len(data)):
            return InvalidMinimumSizeError(data, minimum)

        if not maximum.fits(len(data)):
            return InvalidMaximumSizeError(data, maximum)

        if unique_items and not has_unique_items(data):
            return UniquenessError(data)

        return None

    return validate
