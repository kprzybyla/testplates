__all__ = (
    "struct",
    "create",
    "init",
    "modify",
    "value_of",
    "fields",
    "items",
    "add_codec",
    "field",
    "Field",
    "Structure",
)

from typing import (
    cast,
    overload,
    Any,
    Type,
    TypeVar,
    Tuple,
    Union,
    Iterator,
    Mapping,
    Callable,
    Final,
)

from resultful import (
    Result,
)

from testplates.impl.base import (
    Field as FieldImpl,
    Structure as StructureImpl,
    StructureMeta,
    StructureDict,
    SecretType,
    CodecProtocol,
)

from .value import (
    Maybe,
    Validator,
    MISSING,
)

from .validators import (
    passthrough_validator,
)

from .exceptions import (
    TestplatesError,
)

_GenericType = TypeVar("_GenericType")
_StructureType = TypeVar("_StructureType", bound=StructureImpl)

Field = Union[FieldImpl]
Structure = Union[StructureImpl]

TESTPLATES_CODECS_ATTR_NAME: Final[str] = "_testplates_codecs_"


# noinspection PyTypeChecker
def struct(
    cls: Type[_GenericType],
    /,
) -> Type[Structure]:

    """
    Decorator for creating structure.

    :param cls: any class to be wrapped into structure
    """

    name = cls.__name__
    bases = (cls, StructureImpl)
    attrs = StructureDict(cls.__dict__)
    structure_type = StructureMeta(name, bases, attrs)

    return cast(Type[Structure], structure_type)


# noinspection PyTypeChecker
# noinspection PyShadowingNames
# noinspection PyProtectedMember
def create(
    name: str,
    /,
    **fields: Field[Any],
) -> Type[Structure]:

    """
    Functional API for creating structure.

    :param name: structure type name
    :param fields: structure fields
    """

    structure_type = StructureImpl._testplates_create_(name, **fields)

    return cast(Type[Structure], structure_type)


# noinspection PyProtectedMember
def init(
    structure_type: Type[_StructureType],
    /,
    **values: Any,
) -> Result[_StructureType, TestplatesError]:

    """
    Initializes structure with given values.

    :param structure_type: structure type
    :param values: structure initialization values
    """

    structure = structure_type(SecretType.SECRET)

    return structure._testplates_init_(**values)


# noinspection PyProtectedMember
def modify(
    structure: _StructureType,
    /,
    **values: Any,
) -> Result[_StructureType, TestplatesError]:

    """
    Modifies structure with given values.

    :param structure: structure instance
    :param values: structure modification values
    """

    return structure._testplates_modify_(**values)


# noinspection PyProtectedMember
def value_of(
    structure: Structure,
) -> Mapping[str, Any]:

    """
    Returns structure values.

    :param structure: structure instance
    """

    return dict(structure._testplates_values_)


# noinspection PyProtectedMember
def fields(
    structure_or_structure_type: Union[Structure, Type[Structure]],
    /,
) -> Mapping[str, Field[Any]]:

    """
    Returns structure fields.

    :param structure_or_structure_type: structure type
    """

    return dict(structure_or_structure_type._testplates_fields_)


# noinspection PyShadowingNames
# noinspection PyProtectedMember
def items(
    structure_or_structure_type: Union[Structure, Type[Structure]],
) -> Iterator[Tuple[str, Maybe[_GenericType], Field[_GenericType]]]:

    """
    Returns structure items (name, value, field).

    :param structure_or_structure_type: structure type
    """

    values = structure_or_structure_type._testplates_values_
    fields = structure_or_structure_type._testplates_fields_

    for name, field in fields.items():
        yield name, values.get(name, MISSING), field


def add_codec(
    cls: Type[Structure],
    *,
    codec: Type[CodecProtocol],
) -> None:

    """
    Attaches codec to the given cls.

    :param cls: any class type
    :param codec: codec to be attached to class type
    """

    codecs = getattr(cls, TESTPLATES_CODECS_ATTR_NAME, [])
    codecs.append(codec)


@overload
def field(
    validator: Result[Validator, TestplatesError] = ...,
    /,
    *,
    optional: bool = ...,
) -> Field[_GenericType]:
    ...


@overload
def field(
    validator: Result[Validator, TestplatesError] = ...,
    /,
    *,
    default: _GenericType,
    optional: bool = ...,
) -> Field[_GenericType]:
    ...


@overload
def field(
    validator: Result[Validator, TestplatesError] = ...,
    /,
    *,
    default_factory: Callable[[], _GenericType],
    optional: bool = ...,
) -> Field[_GenericType]:
    ...


def field(
    validator: Result[Validator, TestplatesError] = passthrough_validator(),
    /,
    *,
    default: Maybe[_GenericType] = MISSING,
    default_factory: Maybe[Callable[[], _GenericType]] = MISSING,
    optional: bool = False,
) -> Field[_GenericType]:

    """
    Creates field for structure.

    This is basically a wrapper for :class:`Field`
    with all possible overloads for its arguments.

    :param validator: field validator function or None
    :param default: field default value
    :param default_factory: field default value factory
    :param optional: indication whether field is optional or not
    """

    return Field(
        validator,
        default=default,
        default_factory=default_factory,
        optional=optional,
    )
