__all__ = ["Mapping"]

import typing

from typing import Any, TypeVar, Generic, Iterator

from .value import Maybe, MISSING
from .structure import Structure

_T = TypeVar("_T")


class _Mapping(Generic[_T], Structure[_T], typing.Mapping[str, _T]):

    """
        Mapping-like structure template class.
    """

    __slots__ = ()

    def __getitem__(self, item: str) -> _T:
        return self._values_[item]

    def __iter__(self) -> Iterator[str]:
        return iter(self._values_)

    def __len__(self) -> int:
        return len(self._values_)

    @staticmethod
    def _get_value_(
        self: typing.Mapping[str, _T], key: str, /, *, default: Maybe[_T] = MISSING
    ) -> Maybe[_T]:
        return self.get(key, default)


Mapping = _Mapping[Any]
