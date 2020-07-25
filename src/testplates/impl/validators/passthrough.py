__all__ = ["PassthroughValidator"]

from typing import Any

import testplates

from testplates.impl.base import Result, Success
from testplates.impl.base import TestplatesError


class PassthroughValidator:

    __slots__ = ()

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{type(self).__name__}()"

    def __call__(self, data: Any) -> Result[None, TestplatesError]:
        return Success(None)
