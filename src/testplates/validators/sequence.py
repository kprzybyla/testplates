__all__ = ["sequence_validator"]

import typing

from typing import Any, Optional, Final

import testplates

from testplates.result import Result, Success, Failure
from testplates.boundaries import (
    get_length_boundaries,
    fits_minimum_length,
    fits_maximum_length,
    Edge,
    Boundary,
)

from .utils import has_unique_items, Validator
from .type import type_validator
from .passthrough import passthrough_validator
from .exceptions import (
    ValidationError,
    ItemValidationError,
    InvalidMinimumSizeError,
    InvalidMaximumSizeError,
    UniquenessError,
)

sequence_type_validator: Final[Validator] = Success.get_value(type_validator(typing.Sequence))


class SequenceValidator:

    __slots__ = ("item_validator", "minimum", "maximum", "unique_items")

    def __init__(
        self, item_validator: Validator, minimum: Boundary, maximum: Boundary, unique_items: bool,
    ) -> None:
        self.item_validator = item_validator
        self.minimum = minimum
        self.maximum = maximum
        self.unique_items = unique_items

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{sequence_validator.__name__}()"

    # noinspection PyTypeChecker
    def __call__(self, data: Any) -> Result[None, ValidationError]:
        if (error := sequence_type_validator(data)).is_failure:
            return Failure.from_result(error)

        item_validator = self.item_validator

        for item in data:
            if (error := item_validator(item)).is_failure:
                return Failure(ItemValidationError(error))

        if not fits_minimum_length(data, self.minimum):
            return Failure(InvalidMinimumSizeError(data, self.minimum))

        if not fits_maximum_length(data, self.maximum):
            return Failure(InvalidMaximumSizeError(data, self.maximum))

        if self.unique_items and not has_unique_items(data):
            return Failure(UniquenessError(data))

        return Success(None)


# noinspection PyTypeChecker
def sequence_validator(
    item_validator: Validator = passthrough_validator,
    /,
    *,
    minimum_size: Optional[Edge] = None,
    maximum_size: Optional[Edge] = None,
    unique_items: bool = False,
) -> Result[Validator, ValidationError]:
    result = get_length_boundaries(inclusive_minimum=minimum_size, inclusive_maximum=maximum_size)

    if result.is_failure:
        return Failure.from_result(result)

    minimum, maximum = Success.get_value(result)

    return Success(SequenceValidator(item_validator, minimum, maximum, unique_items))
