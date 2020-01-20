from __future__ import annotations

__all__ = ["Descriptor"]

import abc

from typing import overload, Type, TypeVar, Generic, Union

C = TypeVar("C")
T = TypeVar("T")


class Descriptor(Generic[C, T], abc.ABC):

    __slots__ = ()

    def __set_name__(self, owner: Type[C], name: str) -> None:
        ...

    @overload
    def __get__(self, instance: None, owner: Type[C]) -> Descriptor[C, T]:
        ...

    @overload  # noqa: F811 (https://github.com/PyCQA/pyflakes/issues/320)
    def __get__(self, instance: C, owner: Type[C]) -> T:
        ...

    def __get__(
        self, instance: Union[None, C], owner: Type[C]
    ) -> Union[Descriptor[C, T], T]:  # noqa: F811
        ...

    @property
    @abc.abstractmethod
    def name(self) -> str:
        ...
