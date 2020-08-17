__all__ = ["SequenceValidator"]

import typing

from typing import Any, Union, Final

from resultful import success, failure, unwrap_failure, Result

import testplates

from testplates.impl.base import fits_minimum_length, fits_maximum_length, Limit, UnlimitedType
from testplates.impl.base import TestplatesError

from .utils import has_unique_items, Validator
from .type import TypeValidator
from .exceptions import (
    ItemValidationError,
    InvalidMinimumLengthError,
    InvalidMaximumLengthError,
    UniquenessError,
)

Boundary = Union[UnlimitedType, Limit]

sequence_type_validator: Final[Validator] = TypeValidator(typing.Sequence)


class SequenceValidator:

    __slots__ = ("item_validator", "minimum_length", "maximum_length", "unique_items")

    def __init__(
        self,
        item_validator: Validator,
        /,
        *,
        minimum_length: Boundary,
        maximum_length: Boundary,
        unique_items: bool,
    ) -> None:
        self.item_validator = item_validator
        self.minimum_length = minimum_length
        self.maximum_length = maximum_length
        self.unique_items = unique_items

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{type(self).__name__}()"

    def __call__(self, data: Any, /) -> Result[None, TestplatesError]:
        if not (result := sequence_type_validator(data)):
            return failure(result)

        item_validator = self.item_validator

        for item in data:
            if not (result := item_validator(item)):
                return failure(ItemValidationError(data, item, unwrap_failure(result)))

        if not fits_minimum_length(data, self.minimum_length):
            return failure(InvalidMinimumLengthError(data, self.minimum_length))

        if not fits_maximum_length(data, self.maximum_length):
            return failure(InvalidMaximumLengthError(data, self.maximum_length))

        if self.unique_items and not has_unique_items(data):
            return failure(UniquenessError(data))

        return success(None)
