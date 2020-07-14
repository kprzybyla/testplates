__all__ = ["sequence_validator"]

import typing

from typing import overload, Any, Optional, Final

from testplates.result import Result, Success, Failure
from testplates.boundaries import get_length_boundaries, Edge, Boundary

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

sequence_type_validator: Final[Validator] = type_validator(typing.Sequence).value


class SequenceValidator:

    __slots__ = ("item_validator", "size", "minimum", "maximum", "unique_items")

    def __init__(
        self,
        item_validator: Validator,
        size: Optional[int],
        minimum: Optional[Boundary],
        maximum: Optional[Boundary],
        unique_items: bool,
    ) -> None:
        self.item_validator = item_validator
        self.size = size
        self.minimum = minimum
        self.maximum = maximum
        self.unique_items = unique_items

    def __repr__(self) -> str:
        return f"{sequence_validator.__name__}()"

    def __call__(self, data: Any) -> Result[None, ValidationError]:
        if (error := sequence_type_validator(data)) is not None:
            return Failure.from_result(error)

        item_validator = self.item_validator

        for item in data:
            if (error := item_validator(item)) is not None:
                return Failure(ItemValidationError(error))

        size = self.size

        if size is not None and len(data) != size:
            return Failure(...)

        minimum = self.minimum

        if not minimum.fits(len(data)):
            return Failure(InvalidMinimumSizeError(data, minimum))

        maximum = self.maximum

        if not maximum.fits(len(data)):
            return Failure(InvalidMaximumSizeError(data, maximum))

        if self.unique_items and not has_unique_items(data):
            return Failure(UniquenessError(data))

        return Success(None)


@overload
def sequence_validator(
    item_validator: Validator = ..., /, *, size: Optional[int] = None, unique_items: bool = ...
) -> Result[Validator, ValidationError]:
    ...


@overload
def sequence_validator(
    item_validator: Validator = ...,
    /,
    *,
    minimum_size: Optional[Edge] = None,
    maximum_size: Optional[Edge] = None,
    unique_items: bool = ...,
) -> Result[Validator, ValidationError]:
    ...


def sequence_validator(
    item_validator: Validator = passthrough_validator,
    /,
    *,
    size: Optional[int] = None,
    minimum_size: Optional[Edge] = None,
    maximum_size: Optional[Edge] = None,
    unique_items: bool = False,
) -> Result[Validator, ValidationError]:
    result = get_length_boundaries(inclusive_minimum=minimum_size, inclusive_maximum=maximum_size)

    if result.is_failure:
        return Failure.from_result(result)

    minimum, maximum = result.value

    return Success(SequenceValidator(item_validator, size, minimum, maximum, unique_items))
