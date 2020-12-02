__all__ = ("MappingValidator",)

import typing
import testplates

from typing import (
    Any,
    Type,
    Final,
)

from resultful import (
    success,
    failure,
    unwrap_failure,
    Result,
)

from testplates.impl.base import (
    extract_fields,
    Structure,
)

from testplates.impl.exceptions import (
    TestplatesError,
    RequiredKeyMissingError,
    UnknownFieldError,
    FieldValidationError,
)

from .utils import (
    Validator,
)

from .type import (
    TypeValidator,
)

mapping_type_validator: Final[Validator] = TypeValidator(typing.Mapping)


class MappingValidator:

    __slots__ = ("structure_type",)

    def __init__(
        self,
        structure_type: Type[Structure],
        /,
    ) -> None:
        self.structure_type = structure_type

    def __repr__(self) -> str:
        return f"{testplates.__name__}.mapping_validator({self.structure_type})"

    def __call__(self, data: Any, /) -> Result[None, TestplatesError]:
        if not (result := mapping_type_validator(data)):
            return failure(result)

        structure = self.structure_type
        fields = extract_fields(structure)

        for field in fields.values():
            if not field.is_optional and field.name not in data.keys():
                return failure(RequiredKeyMissingError(data, field.name, field))

        for key, value in data.items():
            field_object = fields.get(key, None)

            if field_object is None:
                return failure(UnknownFieldError(data, structure, key))

            validator = field_object.validator

            if validator is not None and not (result := validator(value)):
                return failure(FieldValidationError(data, field_object, unwrap_failure(result)))

        return success(None)
