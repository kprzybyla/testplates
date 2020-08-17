__all__ = ["MappingValidator"]

import typing

from typing import Any, Final

from resultful import success, failure, unwrap_failure, Result

import testplates

from testplates.impl.base import StructureMeta
from testplates.impl.base import TestplatesError

from .utils import Validator
from .type import TypeValidator
from .exceptions import RequiredKeyMissingError, UnknownKeyError, FieldValidationError

mapping_type_validator: Final[Validator] = TypeValidator(typing.Mapping)


class MappingValidator:

    __slots__ = ("structure_type",)

    def __init__(self, structure_type: StructureMeta[Any], /) -> None:
        self.structure_type = structure_type

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{type(self).__name__}({self.structure_type})"

    # noinspection PyProtectedMember
    def __call__(self, data: Any, /) -> Result[None, TestplatesError]:
        if not (result := mapping_type_validator(data)):
            return failure(result)

        structure = self.structure_type

        for field in structure._fields_.values():
            if not field.is_optional and field.name not in data.keys():
                return failure(RequiredKeyMissingError(data, field.name, field))

        for key, value in data.items():
            field_object = structure._fields_.get(key, None)

            if field_object is None:
                return failure(UnknownKeyError(data, structure, key))

            if not (result := field_object.validator(value)):
                return failure(FieldValidationError(data, field_object, unwrap_failure(result)))

        return success(None)
