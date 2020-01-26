from __future__ import annotations

__all__ = ["Descriptor"]

import abc

from typing import overload, Any, TypeVar, Generic, Union

T = TypeVar("T")


class Descriptor(Generic[T], abc.ABC):

    __slots__ = ()

    def __set_name__(self, owner: Any, name: str) -> None:
        ...

    @overload
    def __get__(self, instance: None, owner: Any) -> Descriptor[T]:
        ...

    @overload  # noqa: F811 (https://github.com/PyCQA/pyflakes/issues/320)
    def __get__(self, instance: Any, owner: Any) -> T:
        ...

    def __get__(
        self, instance: Union[None, Any], owner: Any
    ) -> Union[Descriptor[T], T]:  # noqa: F811
        ...

    @property
    @abc.abstractmethod
    def name(self) -> str:
        ...
