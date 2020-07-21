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

T = TypeVar("T")

Maybe: Final = Union[T, MissingType]
Value: Final = Union[T, SpecialValueType]
Boundary: Final = Union[T, UnlimitedType]

LiteralMissing: Final = Literal[MissingType.MISSING]
LiteralAny: Final = Literal[SpecialValueType.ANY]
LiteralWildcard: Final = Literal[SpecialValueType.WILDCARD]
LiteralAbsent: Final = Literal[SpecialValueType.ABSENT]
LiteralUnlimited: Final = Literal[UnlimitedType.UNLIMITED]

MISSING: Final[LiteralMissing] = MissingType.MISSING
ANY: Final[LiteralAny] = SpecialValueType.ANY
WILDCARD: Final[LiteralWildcard] = SpecialValueType.WILDCARD
ABSENT: Final[LiteralAbsent] = SpecialValueType.ABSENT
UNLIMITED: Final[LiteralUnlimited] = UnlimitedType.UNLIMITED
