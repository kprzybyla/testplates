__all__ = ["initialize", "fields", "field", "Required", "Optional"]

from typing import overload, Any, Type, TypeVar, Union, Mapping, Callable, Literal

from resultful import Result

from testplates.impl.base import Field, Structure

from .value import Value, Maybe, Validator, LiteralAny, LiteralWildcard, LiteralAbsent, MISSING
from .validators import passthrough_validator
from .exceptions import TestplatesError

_T = TypeVar("_T")
_Structure = TypeVar("_Structure", bound=Structure)

Required = Field[Union[_T, LiteralAny]]
Optional = Field[Union[_T, LiteralAny, LiteralWildcard, LiteralAbsent]]


# noinspection PyProtectedMember
def initialize(
    structure: _Structure, /, **values: Value[Any]
) -> Result[_Structure, TestplatesError]:
    return structure._init_(**values)


# noinspection PyProtectedMember
def fields(structure_type: Type[Structure], /) -> Mapping[str, Field[Any]]:
    return dict(structure_type._fields_)


@overload
def field(typ: Type[_T], validator: Validator = ..., /) -> Required[_T]:
    ...


@overload
def field(typ: Type[_T], validator: Validator = ..., /, *, default: _T) -> Required[_T]:
    ...


@overload
def field(
    typ: Type[_T], validator: Validator = ..., /, *, default_factory: Callable[[], _T]
) -> Required[_T]:
    ...


@overload
def field(
    typ: Type[_T], validator: Validator = ..., /, *, optional: Literal[False]
) -> Required[_T]:
    ...


@overload
def field(
    typ: Type[_T], validator: Validator = ..., /, *, default: _T, optional: Literal[False]
) -> Required[_T]:
    ...


@overload
def field(
    typ: Type[_T],
    validator: Validator = ...,
    /,
    *,
    default_factory: Callable[[], _T],
    optional: Literal[False],
) -> Required[_T]:
    ...


@overload
def field(
    typ: Type[_T], validator: Validator = ..., /, *, optional: Literal[True]
) -> Optional[_T]:
    ...


@overload
def field(
    typ: Type[_T], validator: Validator = ..., /, *, default: _T, optional: Literal[True]
) -> Optional[_T]:
    ...


@overload
def field(
    typ: Type[_T],
    validator: Validator = ...,
    /,
    *,
    default_factory: Callable[[], _T],
    optional: Literal[True],
) -> Optional[_T]:
    ...


@overload
def field(
    typ: Type[_T], validator: Validator = ..., /, *, optional: bool = ...
) -> Field[Value[_T]]:
    ...


@overload
def field(
    typ: Type[_T], validator: Validator = ..., /, *, default: _T, optional: bool = ...
) -> Field[Value[_T]]:
    ...


@overload
def field(
    typ: Type[_T],
    validator: Validator = ...,
    /,
    *,
    default_factory: Callable[[], _T],
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

    return Field(validator, default=default, default_factory=default_factory, optional=optional)
