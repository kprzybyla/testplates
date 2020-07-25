__all__ = ["field", "Required", "Optional"]

from typing import overload, TypeVar, Union, Callable, Literal

from testplates.impl.base import Field

from .value import Value, Maybe, MISSING, LiteralAny, LiteralWildcard, LiteralAbsent
from .validators import passthrough_validator, Validator
from .exceptions import InvalidSignatureError

T = TypeVar("T")

Required = Field[Union[T, LiteralAny]]
Optional = Field[Union[T, LiteralAny, LiteralWildcard, LiteralAbsent]]


@overload
def field(validator: Validator = ..., /, *, default: Maybe[T] = ...) -> Required[T]:
    ...


@overload
def field(
    validator: Validator = ..., /, *, default_factory: Maybe[Callable[[], T]] = ...
) -> Required[T]:
    ...


@overload
def field(
    validator: Validator = ..., /, *, default: Maybe[T] = ..., optional: Literal[False]
) -> Required[T]:
    ...


@overload
def field(
    validator: Validator = ...,
    /,
    *,
    default_factory: Maybe[Callable[[], T]] = ...,
    optional: Literal[False],
) -> Required[T]:
    ...


@overload
def field(
    validator: Validator = ..., /, *, default: Maybe[T] = ..., optional: Literal[True]
) -> Optional[T]:
    ...


@overload
def field(
    validator: Validator = ...,
    /,
    *,
    default_factory: Maybe[Callable[[], T]] = ...,
    optional: Literal[True],
) -> Optional[T]:
    ...


@overload
def field(
    validator: Validator = ..., /, *, default: Maybe[T] = ..., optional: bool = ...
) -> Field[Value[T]]:
    ...


@overload
def field(
    validator: Validator = ...,
    /,
    *,
    default_factory: Maybe[Callable[[], T]] = ...,
    optional: bool = ...,
) -> Field[Value[T]]:
    ...


def field(
    validator: Validator = passthrough_validator,
    /,
    *,
    default: Maybe[T] = MISSING,
    default_factory: Maybe[Callable[[], T]] = MISSING,
    optional: bool = False,
) -> Union[Required[T], Optional[T], Field[Value[T]]]:

    """
        Creates field for structure template.

        This is basically a wrapper for :class:`Field`
        with all possible overloads for its arguments.

        :param validator: field validator function or None
        :param default: field default value
        :param default_factory: field default value factory
        :param optional: indication whether field is optional or not
    """

    if default is not MISSING and default_factory is not MISSING:
        raise InvalidSignatureError("Cannot use default and default_factory together")

    return Field(validator, default=default, default_factory=default_factory, optional=optional)
