from typing import TypeVar, Generic

_E = TypeVar("_E", bound=BaseException)

class ExceptionInfo(Generic[_E]):

    value: _E
