__all__ = ["SupportsExclusiveBoundaries", "SupportsInclusiveBoundaries", "SupportsBoundaries"]

from typing import Any
from typing_extensions import runtime_checkable, Protocol


@runtime_checkable
class SupportsExclusiveBoundaries(Protocol):
    def __gt__(self, other: Any) -> bool:

        """
            ...

            :param other:
        """

    def __lt__(self, other: Any) -> bool:

        """
            ...

            :param other:
        """


@runtime_checkable
class SupportsInclusiveBoundaries(Protocol):
    def __ge__(self, other: Any) -> bool:

        """
            ...

            :param other:
        """

    def __le__(self, other: Any) -> bool:

        """
            ...

            :param other:
        """


@runtime_checkable
class SupportsBoundaries(SupportsExclusiveBoundaries, SupportsInclusiveBoundaries, Protocol):
    def __gt__(self, other: Any) -> bool:

        """
            ...

            :param other:
        """

    def __lt__(self, other: Any) -> bool:

        """
            ...

            :param other:
        """

    def __ge__(self, other: Any) -> bool:

        """
            ...

            :param other:
        """

    def __le__(self, other: Any) -> bool:

        """
            ...

            :param other:
        """
