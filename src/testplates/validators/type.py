__all__ = ["type_validator"]

from typing import Any, Tuple, Union

from testplates.result import Result, Success, Failure

from .utils import Validator
from .exceptions import InvalidTypeError


def type_validator(*, allowed_types: Union[type, Tuple[type, ...]]) -> Result[Validator[Any]]:
    def validate(data: Any) -> Result[None]:
        if not isinstance(data, allowed_types):
            return Failure(InvalidTypeError(data, allowed_types))

        return Success(None)

    return Success(validate)
