from __future__ import annotations

__all__ = ["create_object", "CreateObjectFunctionType", "Object"]

from typing import cast, Type, TypeVar, Generic, Protocol

from testplates.impl.base.structure import Field, Structure

from .value import Value, Maybe, MISSING

_T = TypeVar("_T", covariant=True)


# noinspection PyTypeChecker
# noinspection PyProtectedMember
def create_object(name: str, **fields: Field[_T]) -> Type[Object[_T]]:

    """
        Functional API for creating object.

        :param name: object type name
        :param fields: object fields
    """

    return cast(Type[Object[_T]], Object._create_(name, **fields))


class CreateObjectFunctionType(Protocol):
    def __call__(self, name: str, **fields: Field[Value[_T]]) -> Type[Object[_T]]:

        """
            Functional API for creating object.

            :param name: object type name
            :param fields: object fields
        """


class Object(Generic[_T], Structure[_T]):

    """
        Object-like structure template class.
    """

    __slots__ = ()

    @staticmethod
    def _get_value_(
        self: object, key: str, /, *, default: Maybe[_T] = MISSING
    ) -> Value[Maybe[_T]]:
        return cast(Value[Maybe[_T]], getattr(self, key, default))
