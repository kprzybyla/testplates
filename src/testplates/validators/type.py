__all__ = ["type_validator"]

from typing import Any, Tuple, Union, Optional

from .utils import Result, Validator
from .exceptions import InvalidTypeError


def type_validator(*, allowed_types: Union[type, Tuple[type, ...]]) -> Result[Validator[Any]]:
    def validate(data: Any) -> Optional[Exception]:
        if not isinstance(data, allowed_types):
            return InvalidTypeError(data, allowed_types)

        return None

    return validate
