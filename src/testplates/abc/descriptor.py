from __future__ import annotations

__all__ = ["Descriptor"]

import abc

from typing import overload, Type, TypeVar, Generic, Union, Optional

_C = TypeVar("_C")
_T = TypeVar("_T")


class Descriptor(Generic[_C, _T], abc.ABC):

    """
        Abstract non-data descriptor class.
    """

    __slots__ = ()

    @abc.abstractmethod
    def __set_name__(self, owner: Type[_C], name: str) -> None:

        """
            Sets descriptor name upon attachment to parent class.

            :param owner: parent class object
            :param name: descriptor name
        """

    @overload
    def __get__(self, instance: None, owner: Type[_C]) -> Descriptor[_C, _T]:
        ...

    @overload
    def __get__(self, instance: _C, owner: Type[_C]) -> _T:
        ...

    @abc.abstractmethod
    def __get__(self, instance: Optional[_C], owner: Type[_C]) -> Union[Descriptor[_C, _T], _T]:

        """
            Returns either descriptor itself or descriptor value.

            Return value depends on the fact whether descriptor
            was accessed via class object or class instance attribute.

            :param instance: class instance to which descriptor is attached or None
            :param owner: class object to which descriptor is attached
        """

    @property
    @abc.abstractmethod
    def name(self) -> str:

        """
            Returns descriptor name.
        """
