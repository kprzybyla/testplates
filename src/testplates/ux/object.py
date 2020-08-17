from __future__ import annotations

__all__ = ["create_object", "Object"]

from typing import cast, Generic, Type, TypeVar, Mapping, Optional

from testplates.impl.base.structure import Field, Structure

from .value import Maybe, MISSING

_T = TypeVar("_T", covariant=True)


# noinspection PyTypeChecker
# noinspection PyProtectedMember
def create_object(name: str, fields: Optional[Mapping[str, Field[_T]]] = None) -> Type[Object[_T]]:

    """
        Functional API for creating object.

        :param name: object type name
        :param fields: object fields
    """

    return cast(Type[Object[_T]], Object._create_(name, fields))  # type: ignore


class Object(Generic[_T], Structure[_T]):

    """
        Object-like structure template class.
    """

    __slots__ = ()

    @staticmethod
    def _get_value_(self: object, key: str, /, *, default: Maybe[_T] = MISSING) -> Maybe[_T]:
        return cast(Maybe[_T], getattr(self, key, default))
