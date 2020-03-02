__all__ = ["Constraint"]

import abc

from typing import Any


class Constraint(abc.ABC):

    __slots__ = ()

    @abc.abstractmethod
    def __repr__(self) -> str:

        """
            Constraint representation.
        """

    @abc.abstractmethod
    def __eq__(self, other: Any) -> bool:

        """
            Constraint equality conditions and requirements.

            :param other: any other object
        """
