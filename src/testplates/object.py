__all__ = ["Object", "ObjectTemplate"]

from typing import cast, Generic, Any, TypeVar

from .abc import MISSING, Maybe
from .structure import Structure

T = TypeVar("T", covariant=True)


class Object(Generic[T], Structure[T]):

    __slots__ = ()

    @staticmethod
    def _get_value_(self: object, key: str, *, default: Maybe[T] = MISSING) -> Maybe[T]:
        return cast(Maybe[T], getattr(self, key, default))


ObjectTemplate = Object[Any]
