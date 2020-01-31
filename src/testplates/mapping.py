__all__ = ["Mapping", "MappingTemplate"]

import typing

from typing import Any, TypeVar, Generic, Iterator

from .value import MISSING, Maybe
from .structure import Structure

T = TypeVar("T", covariant=True)


class Mapping(Generic[T], Structure[T], typing.Mapping[str, T]):

    __slots__ = ()

    def __getitem__(self, item: str) -> T:
        return self._values_[item]

    def __iter__(self) -> Iterator[str]:
        return iter(self._values_)

    def __len__(self) -> int:
        return len(self._values_)

    @staticmethod
    def _get_value_(
        self: typing.Mapping[str, T], key: str, *, default: Maybe[T] = MISSING
    ) -> Maybe[T]:
        return self.get(key, default)


MappingTemplate = Mapping[Any]
