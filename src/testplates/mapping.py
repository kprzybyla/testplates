from __future__ import annotations

__all__ = (
    "create_mapping",
    "CreateMappingFunctionType",
    "Mapping",
)

import typing

from typing import (
    cast,
    Type,
    TypeVar,
    Generic,
    Iterator,
    Protocol,
)

from testplates.impl.base import (
    Field,
    Structure,
)

from .value import (
    Value,
    Maybe,
    MISSING,
)

_T = TypeVar("_T")
_VT = TypeVar("_VT", covariant=True)


# noinspection PyTypeChecker
# noinspection PyProtectedMember
def create_mapping(name: str, **fields: Field[_VT]) -> Type[Mapping[_VT]]:

    """
    Functional API for creating mapping.

    :param name: mapping type name
    :param fields: mapping fields
    """

    return cast(Type[Mapping[_VT]], Mapping._create_(name, **fields))


class CreateMappingFunctionType(Protocol):
    def __call__(self, name: str, **fields: Field[Value[_VT]]) -> Type[Mapping[_VT]]:

        """
        Functional API for creating mapping.

        :param name: mapping type name
        :param fields: mapping fields
        """


class Mapping(Generic[_VT], Structure, typing.Mapping[str, Value[_VT]]):

    """
    Mapping-like structure template class.
    """

    __slots__ = ()

    def __getitem__(self, item: str) -> Value[_VT]:
        return self._values_[item]

    def __iter__(self) -> Iterator[str]:
        return iter(self._values_)

    def __len__(self) -> int:
        return len(self._values_)

    @staticmethod
    def _get_value_(
        self: Mapping[_T],
        key: str,
        /,
        *,
        default: Maybe[_T] = MISSING,
    ) -> Value[Maybe[_T]]:
        return self.get(key, default)
