__all__ = ["SequenceValidator"]

import typing

from typing import Any, Union, Final

import testplates

from testplates.impl.base import Result, Success, Failure
from testplates.impl.base import fits_minimum_length, fits_maximum_length, Limit, UnlimitedType

from .utils import has_unique_items, Validator
from .type import TypeValidator
from .exceptions import (
    ValidationError,
    ItemValidationError,
    InvalidMinimumSizeError,
    InvalidMaximumSizeError,
    UniquenessError,
)

Boundary = Union[UnlimitedType, Limit]

sequence_type_validator: Final[Validator] = TypeValidator((typing.Sequence,))


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
        return f"{testplates.__name__}.{type(self).__name__}()"

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
