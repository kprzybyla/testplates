from __future__ import annotations

__all__ = ["Descriptor"]

import abc

from typing import overload, Type, TypeVar, Generic, Union, Optional

OwnerType = TypeVar("OwnerType")
ValueType = TypeVar("ValueType")


class Descriptor(Generic[OwnerType, ValueType], abc.ABC):

    """
        Abstract non-data descriptor class.
    """

    __slots__ = ()

    @abc.abstractmethod
    def __set_name__(self, owner: Type[OwnerType], name: str) -> None:

        """
            Sets descriptor name upon attachment to parent class.

            :param owner: parent class object
            :param name: descriptor name
        """

    @overload
    def __get__(self, instance: None, owner: Type[OwnerType]) -> Descriptor[OwnerType, ValueType]:
        ...

    @overload
    def __get__(self, instance: OwnerType, owner: Type[OwnerType]) -> ValueType:
        ...

    @abc.abstractmethod
    def __get__(
        self, instance: Optional[OwnerType], owner: Type[OwnerType]
    ) -> Union[Descriptor[OwnerType, ValueType], ValueType]:

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
