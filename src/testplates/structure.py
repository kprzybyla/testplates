__all__ = (
    "struct",
    "create",
    "init",
    "modify",
    "fields",
    "field",
    "FieldType",
    "StructureType",
    "StructureTypeVar",
)

from typing import (
    cast,
    overload,
    Any,
    Type,
    TypeVar,
    Union,
    Mapping,
    Callable,
)

from resultful import (
    Result,
)

from testplates.impl.base import (
    Field,
    Structure,
    StructureMeta,
    StructureDict,
    SecretType,
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

FieldType = Union[Field]
StructureType = Union[Structure]
StructureTypeVar = TypeVar("StructureTypeVar", bound=Structure)


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
    bases = (cls, Structure)
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

    structure_type = Structure._testplates_create_(name, **fields)

    return cast(Type[Structure], structure_type)


# noinspection PyProtectedMember
def init(
    structure_type: Type[StructureTypeVar],
    /,
    **values: Any,
) -> Result[StructureTypeVar, TestplatesError]:

    """
    Initializes structure with given values.

    :param structure_type: structure type
    :param values: structure initialization values
    """

    structure = structure_type(SecretType.SECRET)

    return structure._testplates_init_(**values)


# noinspection PyProtectedMember
def modify(
    structure: StructureTypeVar,
    /,
    **values: Any,
) -> Result[StructureTypeVar, TestplatesError]:

    """
    Modifies structure with given values.

    :param structure: structure instance
    :param values: structure modification values
    """

    return structure._testplates_modify_(**values)


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
