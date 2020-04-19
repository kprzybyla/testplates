__all__ = ["field", "Required", "Optional"]

from typing import overload, Any, TypeVar, Union, Literal

from .value import Value, Maybe, LiteralAny, LiteralWildcard, LiteralAbsent, MISSING
from .structure import Field

_T = TypeVar("_T")

Required = Field[Union[_T, LiteralAny]]
Optional = Field[Union[_T, LiteralAny, LiteralWildcard, LiteralAbsent]]


@overload
def field() -> Required[Any]:
    ...


@overload
def field(*, default: Maybe[_T] = ...) -> Required[_T]:
    ...


@overload
def field(*, optional: Literal[False]) -> Required[Any]:
    ...


@overload
def field(*, default: Maybe[_T] = ..., optional: Literal[False]) -> Required[_T]:
    ...


@overload
def field(*, optional: Literal[True]) -> Optional[Any]:
    ...


@overload
def field(*, default: Maybe[_T] = ..., optional: Literal[True]) -> Optional[_T]:
    ...


@overload
def field(*, optional: bool = ...) -> Field[Value[Any]]:
    ...


@overload
def field(*, default: Maybe[_T] = ..., optional: bool = ...) -> Field[Value[_T]]:
    ...


def field(
    *, default: Maybe[_T] = MISSING, optional: bool = False
) -> Union[Required[_T], Optional[_T], Field[Value[_T]]]:

    """
        Creates field for structure template.

        This is basically a wrapper for :class:`Field`
        with all possible overloads for its arguments.

        :param default: field default value
        :param optional: indication whether field is optional or not
    """

    return Field(default=default, optional=optional)
