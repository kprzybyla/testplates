__all__ = ["mapping_validator"]

import typing

from typing import Any, TypeVar, Final

import testplates

from testplates.result import Result, Success, Failure
from testplates.base.structure import Structure

from .type import type_validator
from .utils import Validator
from .exceptions import RequiredKeyMissingError, FieldValidationError

_T = TypeVar("_T")

mapping_type_validator: Final[Validator[typing.Mapping]] = type_validator(typing.Mapping).value


class MappingValidator:

    __slots__ = ("structure",)

    def __init__(self, structure: Structure) -> None:
        self.structure = structure

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{mapping_validator.__name__}({self.structure})"

    # noinspection PyProtectedMember
    def __call__(self, data: Any) -> Result[None]:
        if (result := mapping_type_validator(data)).is_error:
            return Failure.from_failure(result)

        structure = self.structure

        for field in structure._fields_.values():
            if not field.is_optional and field.name not in data.keys():
                return Failure(RequiredKeyMissingError(data, field))

        for key, value in data.items():
            field_validator = structure._fields_[key].validator

            if (result := field_validator(value)).is_error:
                return Failure(FieldValidationError(data, key, result))

        return Success(None)


# @lru_cache(maxsize=128, typed=True)
def mapping_validator(structure: Structure) -> Result[Validator[typing.Mapping[str, _T]]]:
    return Success(MappingValidator(structure))
