__all__ = ["ANY", "WILDCARD", "ABSENT", "MISSING", "ValueType", "MissingType", "Value", "Maybe"]

import enum

from typing import TypeVar, Union
from typing_extensions import Literal

T = TypeVar("T")


class ValueType(enum.Enum):

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


class MissingType(enum.Enum):

    MISSING = enum.auto()

    """
        Indicator for missing value.
    """


Value = Union[T, ValueType]
Maybe = Union[T, Literal[MissingType.MISSING]]

ANY: Literal[ValueType.ANY] = ValueType.ANY
WILDCARD: Literal[ValueType.WILDCARD] = ValueType.WILDCARD
ABSENT: Literal[ValueType.ABSENT] = ValueType.ABSENT
MISSING: Literal[MissingType.MISSING] = MissingType.MISSING
