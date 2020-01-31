from __future__ import annotations

__all__ = ["Descriptor"]

import abc

from typing import overload, Any, TypeVar, Generic, Union, Optional

T = TypeVar("T")

# TODO(kprzybyla): Remove noqa (F811) after github.com/PyCQA/pyflakes/issues/320 is delivered


class Descriptor(Generic[T], abc.ABC):

    __slots__ = ()

    def __set_name__(self, owner: Any, name: str) -> None:

        """
            Sets descriptor name upon attachment to parent class.

            :param owner: parent class object
            :param name: descriptor name
        """

    @overload
    def __get__(self, instance: None, owner: Any) -> Descriptor[T]:

        """
            Returns descriptor itself when descriptor is
            accessed via attached class object attribute.

            :param instance: None
            :param owner: class object to which descriptor is attached
        """

    @overload  # noqa
    def __get__(self, instance: Any, owner: Any) -> T:

        """
            Returns descriptor value when descriptor is
            accessed via attached class instance attribute.

            :param instance: class instance to which descriptor is attached
            :param owner: class object to which descriptor is attached
        """

    def __get__(self, instance: Optional[Any], owner: Any) -> Union[Descriptor[T], T]:  # noqa

        """
            Returns either descriptor itself or descriptor value.

            Return value depends on the fact whether descriptor
            was access via class object or class instance attribute.

            :param instance: class instance to which descriptor is attached or None
            :param owner: class object to which descriptor is attached
        """

    @property
    @abc.abstractmethod
    def name(self) -> str:

        """
            Returns descriptor name.
        """
