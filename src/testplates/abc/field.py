__all__ = ["Field"]

import abc

from typing import TypeVar, Generic

from .value import Maybe
from .descriptor import Descriptor

C = TypeVar("C")
T = TypeVar("T")


class Field(Generic[C, T], Descriptor[C, T], abc.ABC):

    __slots__ = ()

    def __repr__(self) -> str:
        return f"Field[{self.name!r}, default={self.default!r}, is_optional={self.is_optional!r}]"

    @property
    @abc.abstractmethod
    def default(self) -> Maybe[T]:
        ...

    @property
    @abc.abstractmethod
    def is_optional(self) -> bool:
        ...

    @abc.abstractmethod
    def validate(self, value: Maybe[T]) -> None:
        ...
