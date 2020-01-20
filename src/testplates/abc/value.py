__all__ = ["ANY", "WILDCARD", "ABSENT", "MissingType", "ValueType", "Missing", "Value", "Maybe"]

import enum

from typing import TypeVar, Union
from typing_extensions import Literal

T = TypeVar("T")


class MissingType:
    def __repr__(self) -> str:
        return "Missing"


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


Missing = MissingType()

Value = Union[T, ValueType]
Maybe = Union[T, MissingType]

ANY: Literal[ValueType.ANY] = ValueType.ANY
WILDCARD: Literal[ValueType.WILDCARD] = ValueType.WILDCARD
ABSENT: Literal[ValueType.ABSENT] = ValueType.ABSENT
