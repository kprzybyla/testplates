from types import TracebackType
from typing import Type, TypeVar, Generic, Union, Tuple, Pattern, Optional

from .code import ExceptionInfo

_E = TypeVar("_E", bound=BaseException)

class RaisesContext(Generic[_E]):
    def __init__(
        self,
        expected_exception: Union[Type[_E], Tuple[Type[_E], ...]],
        message: str,
        match_expr: Optional[Union[str, Pattern[str]]] = None,
    ) -> None: ...
    def __enter__(self) -> ExceptionInfo[_E]: ...
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool: ...

def raises(
    expected_exception: Union[Type[_E], Tuple[Type[_E], ...]],
    *,
    match: Optional[Union[str, Pattern[str]]] = None,
) -> RaisesContext[_E]: ...
