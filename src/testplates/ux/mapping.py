from __future__ import annotations

__all__ = ["create_mapping", "Mapping"]

import typing

from typing import Type, TypeVar, Generic, Iterator, Optional

from testplates.impl.base import Field, Structure

from .value import Maybe, MISSING

T = TypeVar("T", covariant=True)


# noinspection PyProtectedMember
def create_mapping(
    name: str, fields: Optional[typing.Mapping[str, Field[T]]] = None
) -> Type[Mapping[T]]:

    """
        Functional API for creating mapping.

        :param name: mapping type name
        :param fields: mapping fields
    """

    return Mapping._create_(name, fields)


class Mapping(Generic[T], Structure[T], typing.Mapping[str, T]):

    """
        Mapping-like structure template class.
    """

    __slots__ = ()

    def __getitem__(self, item: str) -> T:
        return self._values_[item]

    def __iter__(self) -> Iterator[str]:
        return iter(self._values_)

    def __len__(self) -> int:
        return len(self._values_)

    @staticmethod
    def _get_value_(
        self: typing.Mapping[str, T], key: str, /, *, default: Maybe[T] = MISSING
    ) -> Maybe[T]:
        return self.get(key, default)
