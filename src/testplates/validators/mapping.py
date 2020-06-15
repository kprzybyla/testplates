__all__ = ["mapping_validator"]

import typing

from typing import TypeVar, Optional

from testplates.base.structure import Structure

from .type import type_validator
from .utils import Result, Validator
from .exceptions import RequiredKeyMissingError, FieldValidationError

_T = TypeVar("_T")

validate_mapping_type = type_validator(allowed_types=typing.Mapping)


def mapping_validator(structure: Structure) -> Result[Validator[typing.Mapping[str, _T]]]:
    # noinspection PyProtectedMember
    def validate(data: typing.Mapping[str, _T]) -> Optional[Exception]:
        if (error := validate_mapping_type(data)) is not None:
            return error

        for field in structure._fields_:
            if field.is_optional and field.name not in data.keys():
                return RequiredKeyMissingError(data, field)

        for key, value in data.items():
            validate_field = structure._fields_[key].validator

            if (error := validate_field(value)) is not None:
                return FieldValidationError(data, key, error)

        return None

    return validate
