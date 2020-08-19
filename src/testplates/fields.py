__all__ = ["field", "Required", "Optional"]

from typing import overload, Type, TypeVar, Union, Callable, Literal

from testplates.impl.base import Field

from .value import Value, Maybe, Validator, LiteralAny, LiteralWildcard, LiteralAbsent, MISSING
from .validators import passthrough_validator
from .exceptions import InvalidSignatureError

_T = TypeVar("_T")

Required = Field[Union[_T, LiteralAny]]
Optional = Field[Union[_T, LiteralAny, LiteralWildcard, LiteralAbsent]]


@overload
def field(
    typ: Type[_T], validator: Validator = ..., /, *, default: Maybe[_T] = ...
) -> Required[_T]:
    ...


@overload
def field(
    typ: Type[_T],
    validator: Validator = ...,
    /,
    *,
    default_factory: Maybe[Callable[[], _T]] = ...,
) -> Required[_T]:
    ...


@overload
def field(
    typ: Type[_T],
    validator: Validator = ...,
    /,
    *,
    default: Maybe[_T] = ...,
    optional: Literal[False],
) -> Required[_T]:
    ...


@overload
def field(
    typ: Type[_T],
    validator: Validator = ...,
    /,
    *,
    default_factory: Maybe[Callable[[], _T]] = ...,
    optional: Literal[False],
) -> Required[_T]:
    ...


@overload
def field(
    typ: Type[_T],
    validator: Validator = ...,
    /,
    *,
    default: Maybe[_T] = ...,
    optional: Literal[True],
) -> Optional[_T]:
    ...


@overload
def field(
    typ: Type[_T],
    validator: Validator = ...,
    /,
    *,
    default_factory: Maybe[Callable[[], _T]] = ...,
    optional: Literal[True],
) -> Optional[_T]:
    ...


@overload
def field(
    typ: Type[_T],
    validator: Validator = ...,
    /,
    *,
    default: Maybe[_T] = ...,
    optional: bool = ...,
) -> Field[Value[_T]]:
    ...


@overload
def field(
    typ: Type[_T],
    validator: Validator = ...,
    /,
    *,
    default_factory: Maybe[Callable[[], _T]] = ...,
    optional: bool = ...,
) -> Field[Value[_T]]:
    ...


# noinspection PyUnusedLocal
def field(
    typ: Type[_T],
    validator: Validator = passthrough_validator,
    /,
    *,
    default: Maybe[_T] = MISSING,
    default_factory: Maybe[Callable[[], _T]] = MISSING,
    optional: bool = False,
) -> Union[Required[_T], Optional[_T], Field[Value[_T]]]:

    """
        Creates field for structure template.

        This is basically a wrapper for :class:`Field`
        with all possible overloads for its arguments.

        :param typ: field type
        :param validator: field validator function or None
        :param default: field default value
        :param default_factory: field default value factory
        :param optional: indication whether field is optional or not
    """

    if default is not MISSING and default_factory is not MISSING:
        raise InvalidSignatureError("Cannot use default and default_factory together")

    return Field(validator, default=default, default_factory=default_factory, optional=optional)
