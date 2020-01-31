__all__ = ["SupportsExclusiveBoundaries", "SupportsInclusiveBoundaries", "SupportsBoundaries"]

from typing import Any
from typing_extensions import runtime_checkable, Protocol


@runtime_checkable
class SupportsExclusiveBoundaries(Protocol):

    """
        Protocol for object with exclusive boundaries.
    """

    def __gt__(self, other: Any) -> bool:

        """
            Rich comparison for "greater than".

            :param other: any other object
        """

    def __lt__(self, other: Any) -> bool:

        """
            Rich comparison for "less than".

            :param other: any other object
        """


@runtime_checkable
class SupportsInclusiveBoundaries(Protocol):

    """
        Protocol for object with inclusive boundaries.
    """

    def __ge__(self, other: Any) -> bool:

        """
            Rich comparison for "greater or equal to".

            :param other: any other object
        """

    def __le__(self, other: Any) -> bool:

        """
            Rich comparison for "less or equal to".

            :param other: any other object
        """


@runtime_checkable
class SupportsBoundaries(SupportsExclusiveBoundaries, SupportsInclusiveBoundaries, Protocol):

    """
        Protocol for object with both
        exclusive and inclusive boundaries.
    """
