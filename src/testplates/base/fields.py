__all__ = ["field", "Required", "Optional"]

from typing import overload, Any, TypeVar, Union
from typing_extensions import Literal

from .value import MISSING, Value, Maybe, LiteralAny, LiteralWildcard, LiteralAbsent
from .structure import Field

_T = TypeVar("_T")

Required = Field[Union[_T, LiteralAny]]
Optional = Field[Union[_T, LiteralAny, LiteralWildcard, LiteralAbsent]]

# TODO(kprzybyla): Remove noqa(F811) after github.com/PyCQA/pyflakes/issues/320 is released


@overload
def field() -> Required[Any]:
    ...


@overload  # noqa(F811)
def field(*, default: Maybe[_T] = ...) -> Required[_T]:
    ...


@overload  # noqa(F811)
def field(*, optional: Literal[False]) -> Required[Any]:
    ...


@overload  # noqa(F811)
def field(*, default: Maybe[_T] = ..., optional: Literal[False]) -> Required[_T]:
    ...


@overload  # noqa(F811)
def field(*, optional: Literal[True]) -> Optional[Any]:
    ...


@overload  # noqa(F811)
def field(*, default: Maybe[_T] = ..., optional: Literal[True]) -> Optional[_T]:
    ...


@overload  # noqa(F811)
def field(*, optional: bool = ...) -> Field[Value[Any]]:
    ...


@overload  # noqa(F811)
def field(*, default: Maybe[_T] = ..., optional: bool = ...) -> Field[Value[_T]]:
    ...


def field(  # noqa(F811)
    *, default: Maybe[_T] = MISSING, optional: bool = False
) -> Union[Required[_T], Optional[_T], Field[Value[_T]]]:
    return Field(default=default, optional=optional)