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
    extract_errors,
    extract_fields,
    extract_values,
    extract_codecs,
    extract_codec_metadata,
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

passthrough_validator_singleton: Final[Validator] = PassthroughValidator()


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


def create(
    name: str,
    /,
    **fields_objects: Field[Any],
) -> Type[Structure]:

    """
    Functional API for creating structure.

    :param name: structure type name
    :param fields_objects: structure fields
    """

    cls = cast(StructureMeta, StructureImpl)

    bases = (cls,)
    metaclass = cls.__class__

    attrs = metaclass.__prepare__(name, bases)

    for key, field_object in (fields_objects or {}).items():
        attrs.__setitem__(key, field_object)

    instance = cast(StructureMeta, metaclass.__new__(metaclass, name, bases, attrs))
    metaclass.__init__(instance, name, bases, attrs)

    return cast(Type[Structure], instance)


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

    if errors := extract_errors(structure):
        return failure(InvalidStructureError(errors))

    return success(structure)


def verify(
    structure_or_structure_type: Union[Structure, Type[Structure]],
) -> Result[None, TestplatesError]:

    """
    Verifies structure.

    :param structure_or_structure_type: structure type
    """

    if errors := extract_errors(structure_or_structure_type):
        return failure(InvalidStructureError(errors))

    return success(None)


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

    if errors := extract_errors(structure):
        return failure(InvalidStructureError(errors))

    original_values = extract_values(structure)

    new_values: Dict[str, Any] = dict(original_values)
    new_values.update(values)

    return init(type(structure), **new_values)


def value_of(
    structure: Structure,
) -> Result[Mapping[str, Any], TestplatesError]:

    """
    Returns structure values.

    :param structure: structure instance
    """

    if errors := extract_errors(structure):
        return failure(InvalidStructureError(errors))

    values = extract_values(structure)

    return success(dict(values))


def fields(
    structure_or_structure_type: Union[Structure, Type[Structure]],
    /,
) -> Result[Mapping[str, Field[Any]], TestplatesError]:

    """
    Returns structure fields.

    :param structure_or_structure_type: structure type
    """

    if errors := extract_errors(structure_or_structure_type):
        return failure(InvalidStructureError(errors))

    fields_objects = extract_fields(structure_or_structure_type)

    return success(dict(fields_objects))


def items(
    structure: Structure,
) -> Result[Iterator[Tuple[str, Maybe[Any], Field[Any]]], TestplatesError]:

    """
    Returns structure items (name, value, field).

    :param structure: structure
    """

    if errors := extract_errors(structure):
        return failure(InvalidStructureError(errors))

    values = extract_values(structure)
    fields_objects = extract_fields(structure)

    def iterator() -> Iterator[Tuple[str, Maybe[_GenericType], Field[_GenericType]]]:
        for name, field_object in fields_objects.items():
            yield name, values.get(name, MISSING), field_object

    return success(iterator())


def attach_codec(
    structure_type: Type[Structure],
    *,
    codec: Codec[Any],
    metadata: Optional[_GenericType] = None,
) -> None:

    """
    Attaches codec to the given cls.

    :param structure_type: structure type
    :param codec: codec to be attached to class type
    :param metadata: metadata attached to class type
    """

    if metadata is not None:
        codec_metadata = extract_codec_metadata(codec)
        codec_metadata[structure_type] = metadata

    codecs = extract_codecs(structure_type)
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
