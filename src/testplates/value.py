__all__ = [
    "Maybe",
    "Value",
    "Boundary",
    "LiteralMissing",
    "LiteralAny",
    "LiteralWildcard",
    "LiteralAbsent",
    "LiteralUnlimited",
    "MISSING",
    "ANY",
    "WILDCARD",
    "ABSENT",
    "UNLIMITED",
]

from typing import TypeVar, Union, Literal, Final

from testplates.impl.base import MissingType, SpecialValueType, UnlimitedType

_T = TypeVar("_T")

Maybe = Union[_T, MissingType]
Value = Union[_T, SpecialValueType]
Boundary = Union[_T, UnlimitedType]

LiteralMissing = Literal[MissingType.MISSING]
LiteralAny = Literal[SpecialValueType.ANY]
LiteralWildcard = Literal[SpecialValueType.WILDCARD]
LiteralAbsent = Literal[SpecialValueType.ABSENT]
LiteralUnlimited = Literal[UnlimitedType.UNLIMITED]

MISSING: Final[LiteralMissing] = MissingType.MISSING
ANY: Final[LiteralAny] = SpecialValueType.ANY
WILDCARD: Final[LiteralWildcard] = SpecialValueType.WILDCARD
ABSENT: Final[LiteralAbsent] = SpecialValueType.ABSENT
UNLIMITED: Final[LiteralUnlimited] = UnlimitedType.UNLIMITED
