__all__ = ["passthrough_validator"]

from typing import Any

import testplates

from testplates.result import Result, Success


class PassthroughValidator:

    __slots__ = ()

    def __repr__(self) -> str:
        return f"{testplates.__name__}.passthrough_validator()"

    def __call__(self, data: Any) -> Result[None]:
        return Success(None)


passthrough_validator = PassthroughValidator()
