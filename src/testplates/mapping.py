__all__ = ["Mapping"]

from typing import TypeVar, Generic, Iterator, Mapping as TMapping

from .abc import MissingType, Missing, Maybe
from .structure import Field, Structure

T = TypeVar("T")


class Mapping(Generic[T], Structure[T], TMapping[str, T]):

    __slots__ = ()

    def __class_getitem__(cls, item: str) -> Field[T]:
        return cls._fields_[item]

    def __getitem__(self, item: str) -> T:
        value = self._values_.get(item, Missing)

        if isinstance(value, MissingType):
            try:
                default = self._fields_[item].default
            except KeyError:
                raise KeyError(item)
            else:
                return default

        return value

    def __iter__(self) -> Iterator[str]:
        return iter(self._values_)

    def __len__(self) -> int:
        return len(self._values_)

    @staticmethod
    def _get_value_(self: TMapping[str, T], key: str, *, default: Maybe[T] = Missing) -> Maybe[T]:
        return self.get(key, default)
