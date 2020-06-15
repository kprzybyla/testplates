__all__ = ["field", "Required", "Optional"]

import typing

from typing import overload, TypeVar, Union, Callable, Literal

from .value import Value, Maybe, LiteralAny, LiteralWildcard, LiteralAbsent, MISSING
from .structure import Field

_T = TypeVar("_T")

Required = Field[Union[_T, LiteralAny]]
Optional = Field[Union[_T, LiteralAny, LiteralWildcard, LiteralAbsent]]

Validator = Callable[[_T], Exception]


@overload
def field(
    validator: typing.Optional[Validator[_T]] = ..., /, *, default: Maybe[_T] = ...
) -> Required[_T]:
    ...


@overload
def field(
    validator: typing.Optional[Validator[_T]] = ...,
    /,
    *,
    default: Maybe[_T] = ...,
    optional: Literal[False],
) -> Required[_T]:
    ...


@overload
def field(
    validator: typing.Optional[Validator[_T]] = ...,
    /,
    *,
    default: Maybe[_T] = ...,
    optional: Literal[True],
) -> Optional[_T]:
    ...


@overload
def field(
    validator: typing.Optional[Validator[_T]] = ...,
    /,
    *,
    default: Maybe[_T] = ...,
    optional: bool = ...,
) -> Field[Value[_T]]:
    ...


def field(
    validator: typing.Optional[Validator[_T]] = None,
    /,
    *,
    default: Maybe[_T] = MISSING,
    optional: bool = False,
) -> Union[Required[_T], Optional[_T], Field[Value[_T]]]:

    """
        Creates field for structure template.

        This is basically a wrapper for :class:`Field`
        with all possible overloads for its arguments.

        :param validator: field validator function or None
        :param default: field default value
        :param optional: indication whether field is optional or not
    """

    return Field(validator, default=default, optional=optional)
