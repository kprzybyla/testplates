__all__ = ["mapping_validator"]

import typing

from typing import TypeVar, Iterable, Callable, Optional

from .type import type_validator
from .exceptions import (
    RequiredKeyMissingError,
    RequiredKeyValidatorMissingError,
    FieldValidationError,
)

_T = TypeVar("_T")

validate_mapping_type = type_validator(allowed_types=typing.Mapping)


def mapping_validator(
    required: Iterable[str] = (), /, **fields: Callable[[_T], Optional[Exception]]
) -> Callable[[typing.Mapping[str, _T]], Optional[Exception]]:
    for key in required:
        if key not in fields.keys():
            raise RequiredKeyValidatorMissingError(required, fields)

    def validate(data: typing.Mapping[str, _T]) -> Optional[Exception]:
        if (error := validate_mapping_type(data)) is not None:
            return error

        for key in required:
            if key not in data.keys():
                return RequiredKeyMissingError(data, key)

        for key, value in data.items():
            validate_field = fields[key]

            if (error := validate_field(value)) is not None:
                return FieldValidationError(data, key, error)

        return None

    return validate
