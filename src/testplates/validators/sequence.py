import typing

from typing import Type, TypeVar, Generic, Optional

from testplates.constraints.boundaries import get_length_boundaries

from .base_validator import BaseValidator
from .exceptions import (
    ValidationError,
    ItemValidationError,
    InvalidMinimumSizeError,
    InvalidMaximumSizeError,
    UniquenessError,
)

_T = TypeVar("_T")


def validate_items(validator: BaseValidator[_T], items: typing.Sequence[_T]) -> None:
    if validator is not None:
        for item in items:
            validator.validate(item)


def has_unique_items(items: typing.Sequence[_T]) -> bool:
    visited = set()

    return not any(item in visited or visited.add(item) for item in items)


class Sequence(BaseValidator[typing.Sequence[_T]], Generic[_T]):

    __slots__ = ("_item_validator", "_minimum_size", "_maximum_size", "_unique_items")

    def __init__(
        self,
        item_validator: BaseValidator[_T] = None,
        /,
        *,
        minimum_size: Optional[int] = None,
        maximum_size: Optional[int] = None,
        unique_items: bool = False,
    ) -> None:
        minimum_size, maximum_size = get_length_boundaries(
            inclusive_minimum=minimum_size, inclusive_maximum=maximum_size
        )

        self._item_validator = item_validator
        self._minimum_size = minimum_size
        self._maximum_size = maximum_size
        self._unique_items = unique_items

    @property
    def allowed_types(self) -> Type[typing.Sequence]:
        return typing.Sequence

    def validate(self, data: typing.Sequence[_T]) -> None:
        super().validate(data)

        try:
            validate_items(self._item_validator, data)
        except ValidationError as error:
            raise ItemValidationError(error) from error

        if not self._minimum_size.fits(len(data)):
            raise InvalidMinimumSizeError(data, self._minimum_size)

        if not self._maximum_size.fits(len(data)):
            raise InvalidMaximumSizeError(data, self._maximum_size)

        if self._unique_items and not has_unique_items(data):
            raise UniquenessError(data)
