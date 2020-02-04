__all__ = [
    "ANY",
    "WILDCARD",
    "ABSENT",
    "MISSING",
    "Value",
    "Maybe",
    "LiteralAny",
    "LiteralWildcard",
    "LiteralAbsent",
    "LiteralMissing",
]

import enum

from typing import TypeVar, Union
from typing_extensions import Literal

_T = TypeVar("_T")


class _SpecialValueType(enum.Enum):

    """
        Special value type class.
    """

    ANY = enum.auto()

    """
        Works for both required and optional fields.
        Matches the corresponding field if, and only if, the field value is present.
    """

    WILDCARD = enum.auto()

    """
        Works for optional fields only.
        Matches the corresponding field if either the field value is present or absent.
    """

    ABSENT = enum.auto()

    """
        Works for optional fields only.
        Matches the corresponding field if, and only if, the field value is absent.
    """


class _MissingType(enum.Enum):

    """
        Missing value type class.
    """

    MISSING = enum.auto()

    """
        Indicator for missing value.
    """


LiteralAny = Literal[_SpecialValueType.ANY]
LiteralWildcard = Literal[_SpecialValueType.WILDCARD]
LiteralAbsent = Literal[_SpecialValueType.ABSENT]
LiteralMissing = Literal[_MissingType.MISSING]

Value = Union[_T, _SpecialValueType]
Maybe = Union[_T, LiteralMissing]

ANY: LiteralAny = _SpecialValueType.ANY
WILDCARD: LiteralWildcard = _SpecialValueType.WILDCARD
ABSENT: LiteralAbsent = _SpecialValueType.ABSENT
MISSING: LiteralMissing = _MissingType.MISSING
