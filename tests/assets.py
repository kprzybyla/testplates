__all__ = ["Storage"]

from typing import TypeVar, Dict

_T = TypeVar("_T", covariant=True)


class Storage(Dict[str, _T]):
    def __getattr__(self, item: str) -> _T:
        try:
            return self[item]
        except KeyError:
            raise AttributeError(item) from None
