__all__ = ["field", "Required", "Optional"]

from typing import overload, TypeVar, Union, Literal

from testplates.validators import passthrough_validator
from testplates.validators.utils import Validator

from .value import Value, Maybe, LiteralAny, LiteralWildcard, LiteralAbsent, MISSING
from .structure import Field

_T = TypeVar("_T")

Required = Field[Union[_T, LiteralAny]]
Optional = Field[Union[_T, LiteralAny, LiteralWildcard, LiteralAbsent]]


@overload
def field(validator: Validator = ..., /, *, default: Maybe[_T] = ...) -> Required[_T]:
    ...


@overload
def field(
    validator: Validator = ..., /, *, default: Maybe[_T] = ..., optional: Literal[False]
) -> Required[_T]:
    ...


@overload
def field(
    validator: Validator = ..., /, *, default: Maybe[_T] = ..., optional: Literal[True]
) -> Optional[_T]:
    ...


@overload
def field(
    validator: Validator = ..., /, *, default: Maybe[_T] = ..., optional: bool = ...
) -> Field[Value[_T]]:
    ...


def field(
    validator: Validator = passthrough_validator,
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
