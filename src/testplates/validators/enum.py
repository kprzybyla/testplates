__all__ = ["enum_validator"]

from typing import TypeVar, Mapping, Callable, Optional

from .utils import has_unique_items
from .exceptions import (
    ValidationError,
    MemberValidationError,
    ProhibitedValueError,
    EnumAliasesNotAllowed,
)

_T = TypeVar("_T")


def enum_validator(
    validate_member_value: Callable[[_T], Optional[Exception]],
    members: Mapping[str, _T],
    /,
    *,
    allow_aliases: bool = True,
) -> Callable[[_T], Optional[Exception]]:
    for value in members.values():
        error = validate_member_value(value)

        if error is not None:
            raise error

    if not allow_aliases and not has_unique_items(members.values()):
        raise EnumAliasesNotAllowed()

    def validate(data: _T) -> Optional[Exception]:
        if (error := validate_member_value(data)) is not None:
            return MemberValidationError(error)

        values = members.values()

        if data not in values:
            return ProhibitedValueError(data, values)

        return None

    return validate
