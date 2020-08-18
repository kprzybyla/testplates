__all__ = ["PassthroughValidator"]

from typing import Any

from resultful import success, Result

import testplates

from testplates.impl.base import TestplatesError


class PassthroughValidator:

    __slots__ = ()

    def __repr__(self) -> str:
        return f"{testplates.__name__}.passthrough_validator()"

    def __call__(self, data: Any, /) -> Result[None, TestplatesError]:
        return success(None)
