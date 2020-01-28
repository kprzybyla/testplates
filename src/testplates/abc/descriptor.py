from __future__ import annotations

__all__ = ["Descriptor"]

import abc

from typing import overload, Any, TypeVar, Generic, Union

T = TypeVar("T")


class Descriptor(Generic[T], abc.ABC):

    __slots__ = ()

    def __set_name__(self, owner: Any, name: str) -> None:

        """
            ...

            :param owner:
            :param name:
        """

    @overload
    def __get__(self, instance: None, owner: Any) -> Descriptor[T]:

        """
            ...

            :param instance:
            :param owner:
        """

    @overload  # noqa: F811 (https://github.com/PyCQA/pyflakes/issues/320)
    def __get__(self, instance: Any, owner: Any) -> T:

        """
            ...

            :param instance:
            :param owner:
        """

    def __get__(
        self, instance: Union[None, Any], owner: Any
    ) -> Union[Descriptor[T], T]:  # noqa: F811

        """
            ...

            :param instance:
            :param owner:
        """

    @property
    @abc.abstractmethod
    def name(self) -> str:

        """
            ...
        """
