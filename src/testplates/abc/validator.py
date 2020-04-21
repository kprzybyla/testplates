__all__ = ["Validator"]

import abc

from typing import TypeVar, Generic

_T = TypeVar("_T")


class Validator(abc.ABC, Generic[_T]):

    """
        Abstract validator class.
    """

    __slots__ = ()

    @abc.abstractmethod
    def validate(self, data: _T) -> None:

        """
            Validates data.

            :param data: data to be validated
        """
