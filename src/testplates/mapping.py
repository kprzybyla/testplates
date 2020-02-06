__all__ = ["Mapping"]

import typing

from typing import TypeVar, Generic, Iterator

from .value import MISSING, Maybe
from .structure import Structure

_T = TypeVar("_T", covariant=True)


class Mapping(Generic[_T], Structure[_T], typing.Mapping[str, _T]):

    __slots__ = ()

    def __getitem__(self, item: str) -> _T:
        return self._values_[item]

    def __iter__(self) -> Iterator[str]:
        return iter(self._values_)

    def __len__(self) -> int:
        return len(self._values_)

    @staticmethod
    def _get_value_(
        self: typing.Mapping[str, _T], key: str, *, default: Maybe[_T] = MISSING
    ) -> Maybe[_T]:
        return self.get(key, default)
