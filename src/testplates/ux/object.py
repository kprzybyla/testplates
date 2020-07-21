__all__ = ["create_object", "Object"]

import typing

from typing import cast, Generic, TypeVar

from testplates.impl.base.structure import Field, Structure, StructureMeta

from .value import Maybe, MISSING

T = TypeVar("T", covariant=True)


# noinspection PyProtectedMember
def create_object(name: str, fields: typing.Mapping[str, Field[T]] = None) -> StructureMeta[T]:

    """
        Functional API for creating object.

        :param name: object type name
        :param fields: object fields
    """

    return Object._create_(name, fields)


class Object(Generic[T], Structure[T]):

    """
        Object-like structure template class.
    """

    __slots__ = ()

    @staticmethod
    def _get_value_(self: object, key: str, /, *, default: Maybe[T] = MISSING) -> Maybe[T]:
        return cast(Maybe[T], getattr(self, key, default))
