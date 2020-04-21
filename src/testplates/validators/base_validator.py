__all__ = ["BaseValidator"]

from typing import Type, TypeVar, Generic, Optional

from testplates.abc import Validator

from .exceptions import InvalidTypeError

_T = TypeVar("_T")


class BaseValidator(Validator[_T], Generic[_T]):

    __slots__ = ()

    @property
    def allowed_types(self) -> Optional[Type[_T]]:
        return None

    def validate(self, data: _T) -> None:
        allowed_types = self.allowed_types

        if allowed_types is not None and not isinstance(data, allowed_types):
            raise InvalidTypeError(data, allowed_types)
