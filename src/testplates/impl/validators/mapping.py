__all__ = ["MappingValidator"]

import typing

from typing import Any, Final

import testplates

from testplates.impl.base import Result, Success, Failure, StructureMeta
from testplates.impl.base import TestplatesError

from .utils import Validator
from .type import TypeValidator
from .exceptions import RequiredKeyMissingError, FieldValidationError

mapping_type_validator: Final[Validator] = TypeValidator((typing.Mapping,))


class MappingValidator:

    __slots__ = ("structure_type",)

    def __init__(self, structure_type: StructureMeta) -> None:
        self.structure_type = structure_type

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{type(self).__name__}({self.structure_type})"

    # noinspection PyTypeChecker
    # noinspection PyProtectedMember
    def __call__(self, data: Any) -> Result[None, TestplatesError]:
        if (result := mapping_type_validator(data)).is_failure:
            return Failure.from_result(result)

        structure = self.structure_type

        for field in structure._fields_.values():
            if not field.is_optional and field.name not in data.keys():
                return Failure(RequiredKeyMissingError(data, field.name, field))

        for key, value in data.items():
            field = structure._fields_[key]

            if (result := field.validator(value)).is_failure:
                return Failure(FieldValidationError(data, field, result))

        return Success(None)
