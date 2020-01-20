__all__ = ["Object"]

from typing import cast, TypeVar, Generic

from .abc import Missing, Maybe
from .structure import Structure

T = TypeVar("T")


class Object(Generic[T], Structure[T]):

    __slots__ = ()

    @staticmethod
    def _get_value_(self: object, key: str, *, default: Maybe[T] = Missing) -> Maybe[T]:
        return cast(Maybe[T], getattr(self, key, default))
