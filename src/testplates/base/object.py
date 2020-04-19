__all__ = ["Object"]

from typing import cast, Any, Generic, TypeVar

from .value import Maybe, MISSING
from .structure import Structure

_T = TypeVar("_T")


class _Object(Generic[_T], Structure[_T]):

    """
        Object-like structure template class.
    """

    __slots__ = ()

    @staticmethod
    def _get_value_(self: object, key: str, /, *, default: Maybe[_T] = MISSING) -> Maybe[_T]:
        return cast(Maybe[_T], getattr(self, key, default))


Object = _Object[Any]
