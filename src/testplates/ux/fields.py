__all__ = ["field", "Required", "Optional"]

from typing import overload, TypeVar, Union, Literal, Final

from testplates.impl.base import Field

from .value import Value, Maybe, MISSING, LiteralAny, LiteralWildcard, LiteralAbsent
from .validators import passthrough_validator, Validator

T = TypeVar("T")

Required: Final = Field[Union[T, LiteralAny]]
Optional: Final = Field[Union[T, LiteralAny, LiteralWildcard, LiteralAbsent]]


@overload
def field(validator: Validator = ..., /, *, default: Maybe[T] = ...) -> Required[T]:
    ...


@overload
def field(
    validator: Validator = ..., /, *, default: Maybe[T] = ..., optional: Literal[False]
) -> Required[T]:
    ...


@overload
def field(
    validator: Validator = ..., /, *, default: Maybe[T] = ..., optional: Literal[True]
) -> Optional[T]:
    ...


@overload
def field(
    validator: Validator = ..., /, *, default: Maybe[T] = ..., optional: bool = ...
) -> Field[Value[T]]:
    ...


def field(
    validator: Validator = passthrough_validator,
    /,
    *,
    default: Maybe[T] = MISSING,
    optional: bool = False,
) -> Union[Required[T], Optional[T], Field[Value[T]]]:

    """
        Creates field for structure template.

        This is basically a wrapper for :class:`Field`
        with all possible overloads for its arguments.

        :param validator: field validator function or None
        :param default: field default value
        :param optional: indication whether field is optional or not
    """

    return Field(validator, default=default, optional=optional)
