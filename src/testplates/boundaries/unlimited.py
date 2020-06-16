__all__ = ["LiteralUnlimited", "UNLIMITED"]

import enum

from typing import Literal

import testplates


class _UnlimitedType(enum.Enum):

    """
        Unlimited value type class.
    """

    UNLIMITED = enum.auto()

    """
        Indicator for unlimited value.
    """

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{self.name}"


LiteralUnlimited = Literal[_UnlimitedType.UNLIMITED]

UNLIMITED: LiteralUnlimited = _UnlimitedType.UNLIMITED
