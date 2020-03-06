from types import TracebackType
from typing import Any, Type, TypeVar, Generic, Union, Tuple, Pattern, Optional  # noqa

# TODO(kprzybyla): Remove noqa (F401) after github.com/PyCQA/pyflakes/issues/447 is released

_E = TypeVar("_E", bound=BaseException)


class ExceptionInfo(Generic[_E]):
    ...


class RaisesContext(Generic[_E]):
    def __enter__(self) -> ExceptionInfo[_E]:
        ...

    def __exit__(
        self,
        exc_type: Optional["Type[BaseException]"],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        ...


def raises(
    expected_exception: Union["Type[_E]", Tuple["Type[_E]", ...]],
    *args: Any,
    match: Optional[Union[str, "Pattern[str]"]] = None,
    **kwargs: Any,
) -> "RaisesContext[_E]":
    ...
