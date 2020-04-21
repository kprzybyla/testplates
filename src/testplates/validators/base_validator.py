__all__ = ["BaseValidator"]

from typing import TypeVar, Generic

from testplates.abc import Validator

_T = TypeVar("_T")


class BaseValidator(Validator[_T], Generic[_T]):

    __slots__ = ()

    def validate(self, data: _T) -> None:
        pass
