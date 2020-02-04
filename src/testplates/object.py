__all__ = ["Object", "ObjectTemplate"]

from typing import cast, Generic, Any, TypeVar

from .value import MISSING, Maybe
from .structure import Structure

_T = TypeVar("_T", covariant=True)


class Object(Generic[_T], Structure[_T]):

    __slots__ = ()

    @staticmethod
    def _get_value_(self: object, key: str, *, default: Maybe[_T] = MISSING) -> Maybe[_T]:
        return cast(Maybe[_T], getattr(self, key, default))


ObjectTemplate = Object[Any]
