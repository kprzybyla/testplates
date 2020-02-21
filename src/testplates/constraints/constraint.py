__all__ = ["Constraint"]

import abc

from typing import Any


class Constraint(abc.ABC):

    __slots__ = ()

    def __repr__(self) -> str:
        return f"{type(self).__name__}[]"

    @abc.abstractmethod
    def __eq__(self, other: Any) -> bool:

        """
            ...

            :param other:
        """
