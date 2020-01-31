__all__ = ["Required", "Optional"]

from typing import TypeVar, Union
from typing_extensions import Literal as L

from .abc import ValueType
from .structure import Field

T = TypeVar("T")

Required = Field[Union[T, L[ValueType.ANY]]]
Optional = Field[Union[T, L[ValueType.ANY], L[ValueType.WILDCARD], L[ValueType.ABSENT]]]
