from __future__ import annotations

__all__ = ["create_mapping", "Mapping"]

import typing

from typing import cast, Type, TypeVar, Generic, Iterator, Optional

from testplates.impl.base import Field, Structure

from .value import Maybe, MISSING

_T = TypeVar("_T", covariant=True)


# noinspection PyTypeChecker
# noinspection PyProtectedMember
def create_mapping(
    name: str, fields: Optional[typing.Mapping[str, Field[_T]]] = None
) -> Type[Mapping[_T]]:

    """
        Functional API for creating mapping.

        :param name: mapping type name
        :param fields: mapping fields
    """

    return cast(Type[Mapping[_T]], Mapping._create_(name, fields))  # type: ignore


class Mapping(Generic[_T], Structure[_T], typing.Mapping[str, _T]):

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
