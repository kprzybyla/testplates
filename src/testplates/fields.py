__all__ = ["Required", "Optional"]

from typing import TypeVar, Union
from typing_extensions import Literal

from .abc import ValueType
from .structure import Field

T = TypeVar("T")

_ANY = Literal[ValueType.ANY]
_WILDCARD = Literal[ValueType.WILDCARD]
_ABSENT = Literal[ValueType.ABSENT]

Required = Field[Union[T, _ANY]]
Optional = Field[Union[T, _ANY, _WILDCARD, _ABSENT]]
