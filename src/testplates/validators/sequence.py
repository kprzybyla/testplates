__all__ = ["sequence_validator"]

import typing

from typing import TypeVar, Callable, Optional

from testplates.constraints.boundaries import get_length_boundaries

from .type import type_validator, validate_any
from .utils import has_unique_items
from .exceptions import (
    ItemValidationError,
    InvalidMinimumSizeError,
    InvalidMaximumSizeError,
    UniquenessError,
)

_T = TypeVar("_T")

validate_sequence_type = type_validator(allowed_types=typing.Sequence)


def sequence_validator(
    validate_item: Callable[[_T], Optional[Exception]] = validate_any,
    /,
    *,
    minimum_size: Optional[int] = None,
    maximum_size: Optional[int] = None,
    unique_items: bool = False,
) -> Callable[[typing.Sequence[_T]], Optional[Exception]]:
    minimum, maximum = get_length_boundaries(
        inclusive_minimum=minimum_size, inclusive_maximum=maximum_size
    )

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
