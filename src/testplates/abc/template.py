__all__ = ["Template"]

import abc

from typing import Any


class Template(abc.ABC):

    __slots__ = ()

    @abc.abstractmethod
    def __repr__(self) -> str:

        """
            Template representation.
        """

    @abc.abstractmethod
    def __eq__(self, other: Any) -> bool:

        """
            Template equality conditions and requirements.

            :param other: any other object
        """
