__all__ = ["Object"]

from typing import cast, Any, Generic, TypeVar

from .value import MISSING, Maybe
from .structure import Structure

_T = TypeVar("_T", covariant=True)


class _Object(Generic[_T], Structure[_T]):

    __slots__ = ()

    @staticmethod
    def _get_value_(self: object, key: str, *, default: Maybe[_T] = MISSING) -> Maybe[_T]:
        return cast(Maybe[_T], getattr(self, key, default))


Object = _Object[Any]
