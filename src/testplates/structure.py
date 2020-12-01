__all__ = (
    "struct",
    "create",
    "init",
    "verify",
    "modify",
    "value_of",
    "fields",
    "items",
    "attach_codec",
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
    Dict,
    Callable,
    Optional,
    Final,
)

from resultful import (
    Result,
    success,
    failure,
    unwrap_success,
    unwrap_failure,
)

from testplates.impl.base import (
    Codec as CodecImpl,
    Field as FieldImpl,
    Structure as StructureImpl,
    StructureMeta,
    StructureDict,
)

from testplates.impl.validators import (
    PassthroughValidator,
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
    InvalidStructureError,
)

_GenericType = TypeVar("_GenericType")
_StructureType = TypeVar("_StructureType", bound=StructureImpl)

Codec = Union[CodecImpl]
Field = Union[FieldImpl]
Structure = Union[StructureImpl]

TESTPLATES_CODECS_ATTR_NAME: Final[str] = "_testplates_codecs_"
TESTPLATES_METADATA_STORAGE_ATTR_NAME: Final[str] = "_testplates_metadata_storage_"

passthrough_validator_singleton: Final[Validator] = PassthroughValidator()


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

    cls = cast(StructureMeta, StructureImpl)

    bases = (cls,)
    metaclass = cls.__class__

    attrs = metaclass.__prepare__(name, bases)

    for key, field in (fields or {}).items():
        attrs.__setitem__(key, field)

    instance = cast(StructureMeta, metaclass.__new__(metaclass, name, bases, attrs))
    metaclass.__init__(instance, name, bases, attrs)

    return cast(Type[Structure], instance)


# noinspection PyShadowingNames
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

    structure = structure_type(**values)

    if errors := structure._testplates_errors_:
        return failure(InvalidStructureError(errors))

    return success(structure)


# noinspection PyProtectedMember
def verify(
    structure_or_structure_type: Union[Structure, Type[Structure]],
) -> Result[None, TestplatesError]:

    """
    Verifies structure.

    :param structure_or_structure_type: structure type
    """

    if errors := structure_or_structure_type._testplates_errors_:
        return failure(InvalidStructureError(errors))

    return success(None)


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

    if errors := structure._testplates_errors_:
        return failure(InvalidStructureError(errors))

    original_values = structure._testplates_values_

    new_values: Dict[str, Any] = dict(original_values)
    new_values.update(values)

    return init(type(structure), **new_values)


# noinspection PyProtectedMember
def value_of(
    structure: Structure,
) -> Result[Mapping[str, Any], TestplatesError]:

    """
    Returns structure values.

    :param structure: structure instance
    """

    if errors := structure._testplates_errors_:
        return failure(InvalidStructureError(errors))

    values = structure._testplates_values_

    return success(dict(values))


# noinspection PyShadowingNames
# noinspection PyProtectedMember
def fields(
    structure_or_structure_type: Union[Structure, Type[Structure]],
    /,
) -> Result[Mapping[str, Field[Any]], TestplatesError]:

    """
    Returns structure fields.

    :param structure_or_structure_type: structure type
    """

    if errors := structure_or_structure_type._testplates_errors_:
        return failure(InvalidStructureError(errors))

    fields = structure_or_structure_type._testplates_fields_

    return success(dict(fields))


# noinspection PyShadowingNames
# noinspection PyProtectedMember
def items(
    structure_or_structure_type: Union[Structure, Type[Structure]],
) -> Result[Iterator[Tuple[str, Maybe[Any], Field[Any]]], TestplatesError]:

    """
    Returns structure items (name, value, field).

    :param structure_or_structure_type: structure type
    """

    if errors := structure_or_structure_type._testplates_errors_:
        return failure(InvalidStructureError(errors))

    values = structure_or_structure_type._testplates_values_
    fields = structure_or_structure_type._testplates_fields_

    # noinspection PyShadowingNames
    def iterator() -> Iterator[Tuple[str, Maybe[_GenericType], Field[_GenericType]]]:
        for name, field in fields.items():
            yield name, values.get(name, MISSING), field

    return success(iterator())


def attach_codec(
    cls: Type[Structure],
    *,
    codec: Codec[Any],
    metadata: Optional[_GenericType] = None,
) -> None:

    """
    Attaches codec to the given cls.

    :param cls: any class type
    :param codec: codec to be attached to class type
    :param metadata: metadata attached to class type
    """

    if metadata is not None:
        metadata_storage = getattr(codec, TESTPLATES_METADATA_STORAGE_ATTR_NAME, {})
        metadata_storage[cls] = metadata

    codecs = getattr(cls, TESTPLATES_CODECS_ATTR_NAME, [])
    codecs.append(codec)


@overload
def field(
    validator: Result[Validator, TestplatesError] = ...,
    /,
    *,
    optional: bool = ...,
) -> Field[Any]:
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


# noinspection PyTypeChecker
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

    if not validator:
        return Field(
            passthrough_validator_singleton,
            default=default,
            default_factory=default_factory,
            optional=optional,
            errors=[unwrap_failure(validator)],
        )

    return Field(
        unwrap_success(validator),
        default=default,
        default_factory=default_factory,
        optional=optional,
    )
