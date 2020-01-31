__all__ = ["Field"]

import abc

from typing import TypeVar, Generic

from .value import Maybe
from .descriptor import Descriptor

T = TypeVar("T")


class Field(Generic[T], Descriptor[T], abc.ABC):

    __slots__ = ()

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}"
            f"[{self.name!r}, default={self.default!r}, is_optional={self.is_optional!r}]"
        )

    @property
    @abc.abstractmethod
    def default(self) -> Maybe[T]:

        """
            Returns field default value.

            If the field does not have a default value,
            missing value indicator is returned instead.
        """

    @property
    @abc.abstractmethod
    def is_optional(self) -> bool:

        """
            Returns True if field is optional, otherwise False.
        """

    @abc.abstractmethod
    def validate(self, value: Maybe[T]) -> None:

        """
            Validates the given value against the field.

            :param value: value to be validated
        """
