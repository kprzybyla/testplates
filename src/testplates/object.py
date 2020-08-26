from __future__ import annotations

__all__ = (
    "create_object",
    "CreateObjectFunctionType",
    "Object",
)

from typing import (
    cast,
    Any,
    Type,
    TypeVar,
    Protocol,
)

from testplates.impl.base.structure import (
    Field,
    Structure,
)

from .value import (
    Value,
    Maybe,
    MISSING,
)

_T = TypeVar("_T")


# noinspection PyTypeChecker
# noinspection PyProtectedMember
def create_object(name: str, **fields: Field[Any]) -> Type[Object]:

    """
    Functional API for creating object.

    :param name: object type name
    :param fields: object fields
    """

    return cast(Type[Object], Object._testplates_create_(name, **fields))


class CreateObjectFunctionType(Protocol):
    def __call__(self, name: str, **fields: Field[Value[Any]]) -> Type[Object]:

        """
        Functional API for creating object.

        :param name: object type name
        :param fields: object fields
        """


class Object(Structure):

    """
    Object-like structure template class.
    """

    __slots__ = ()

    @staticmethod
    def _testplates_get_value_(
        self: object,
        key: str,
        /,
        *,
        default: Maybe[_T] = MISSING,
    ) -> Value[Maybe[_T]]:
        return cast(Value[Maybe[_T]], getattr(self, key, default))
