from __future__ import annotations

__all__ = (
    "Codec",
    "EncodeFunction",
    "DecodeFunction",
    "Field",
    "Structure",
    "StructureMeta",
    "StructureDict",
)

import abc
import testplates

from typing import (
    cast,
    overload,
    Any,
    Type,
    TypeVar,
    Generic,
    ClassVar,
    Union,
    Tuple,
    List,
    Dict,
    Iterator,
    Mapping,
    MutableMapping,
    Callable,
    Optional,
    Protocol,
    Final,
)

from resultful import (
    success,
    failure,
    unwrap_failure,
    Result,
)

from testplates.impl.utils import (
    format_like_dict,
)

from testplates.impl.exceptions import (
    TestplatesError,
    MissingValueError,
    UnexpectedValueError,
    ProhibitedValueError,
)

from .value import (
    is_value,
    values_matches,
    Maybe,
    Validator,
    MISSING,
    ANY,
    WILDCARD,
    ABSENT,
)

# noinspection PyTypeChecker
_Structure = TypeVar("_Structure", bound="Structure")
_GenericType = TypeVar("_GenericType")
_CovariantType = TypeVar("_CovariantType", covariant=True)
_ContravariantType = TypeVar("_ContravariantType", contravariant=True)

TESTPLATES_ERRORS_ATTR_NAME: Final[str] = "_testplates_errors_"
TESTPLATES_CODECS_ATTR_NAME: Final[str] = "_testplates_codecs_"
TESTPLATES_DEFAULT_CODEC_ATTR_NAME: Final[str] = "_testplates_default_codec_"

Metadata = Mapping[Type["Structure"], _CovariantType]
MetadataStorage = MutableMapping[Type["Structure"], _CovariantType]


class EncodeFunction(Protocol[_ContravariantType]):
    def __call__(
        self,
        metadata: _ContravariantType,
        structure: Structure,
    ) -> Result[bytes, TestplatesError]:

        """
        Encodes structure into bytes.

        :param structure: structure to be encoded
        """


class DecodeFunction(Protocol[_ContravariantType]):
    def __call__(
        self,
        metadata: _ContravariantType,
        structure_type: Type[_Structure],
        data: bytes,
    ) -> Result[_Structure, TestplatesError]:

        """
        Decodes bytes into structure.

        :param structure_type: structure type to be decoded to
        :param data: bytes to be decoded
        """


class Codec(Generic[_GenericType]):

    __slots__ = (
        "_encode_function",
        "_decode_function",
        "_testplates_metadata_storage_",
    )

    def __init__(
        self,
        encode_function: EncodeFunction[_GenericType],
        decode_function: DecodeFunction[_GenericType],
    ):
        self._encode_function = encode_function
        self._decode_function = decode_function

        self._testplates_metadata_storage_: MetadataStorage[_GenericType] = {}

    @property
    def metadata(self) -> Metadata[_GenericType]:
        return self._testplates_metadata_storage_

    @property
    def encode_function(self) -> EncodeFunction[_GenericType]:
        return self._encode_function

    @property
    def decode_function(self) -> DecodeFunction[_GenericType]:
        return self._decode_function


class Field(Generic[_CovariantType]):

    """
    Field descriptor class.
    """

    __slots__ = (
        "_validator",
        "_errors",
        "_default",
        "_default_factory",
        "_optional",
        "_name",
    )

    def __init__(
        self,
        validator: Validator,
        /,
        *,
        default: Maybe[_CovariantType] = MISSING,
        default_factory: Maybe[Callable[[], _CovariantType]] = MISSING,
        optional: bool = False,
        errors: Optional[List[TestplatesError]] = None,
    ) -> None:
        self._validator = validator
        self._errors: List[TestplatesError] = []
        self._default = default
        self._default_factory = default_factory
        self._optional = optional
        self._errors = errors or []

    def __repr__(self) -> str:
        parameters = [f"{self._name!r}"]

        if (default := self.default) is not MISSING:
            parameters.append(f"default={default!r}")

        parameters.append(f"optional={self.is_optional!r}")

        return f"{testplates.__name__}.{type(self).__name__}({', '.join(parameters)})"

    def __set_name__(
        self,
        owner: Callable[..., Structure],
        name: str,
    ) -> None:
        self._name = name

    @overload
    def __get__(
        self,
        instance: None,
        owner: Callable[..., Structure],
    ) -> Field[_CovariantType]:
        ...

    @overload
    def __get__(
        self,
        instance: Structure,
        owner: Callable[..., Structure],
    ) -> _CovariantType:
        ...

    # noinspection PyProtectedMember
    def __get__(
        self,
        instance: Optional[Structure],
        owner: Callable[..., Structure],
    ) -> Union[Field[_CovariantType], _CovariantType]:

        """
        Returns either field itself or field value.

        Return value depends on the fact whether field was accessed
        via :class:`Structure` class object or class instance attribute.

        :param instance: :class:`Structure` class instance to which field is attached or None
        :param owner: :class:`Structure` class object to which field is attached
        """

        if instance is None:
            return self

        return cast(_CovariantType, instance._testplates_values_[self.name])

    @property
    def name(self) -> str:

        """
        Returns field name.
        """

        return self._name

    @property
    def validator(self) -> Optional[Validator]:

        """
        Returns field validator function.
        """

        return self._validator

    @property
    def errors(self) -> List[TestplatesError]:

        """
        Returns field errors list.
        """

        return self._errors

    # noinspection PyCallingNonCallable
    @property
    def default(self) -> Maybe[_CovariantType]:

        """
        Returns field default value.

        If the field does not have a default value,
        missing value indicator is returned instead.
        """

        default_factory = self._default_factory

        if default_factory is not MISSING:
            return default_factory()

        return self._default

    @property
    def is_optional(self) -> bool:

        """
        Returns True if field is optional, otherwise False.
        """

        return self._optional

    # noinspection PyUnboundLocalVariable
    def validate(
        self,
        value: Maybe[_CovariantType],
        /,
    ) -> Result[None, TestplatesError]:

        """
        Validates the given value against the field requirements.

        :param value: value to be validated
        """

        validator = self.validator
        default = self.default
        is_optional = self.is_optional

        if value is ANY:
            return success(None)

        elif value is MISSING and default is MISSING:
            return failure(MissingValueError(self))

        elif (value is ABSENT or default is ABSENT) and not is_optional:
            return failure(ProhibitedValueError(self, value))

        elif (value is WILDCARD or default is WILDCARD) and not is_optional:
            return failure(ProhibitedValueError(self, value))

        elif is_value(value) and validator is not None and not (result := validator(value)):
            return result

        return success(None)


class StructureDict(Dict[str, Any]):

    __slots__ = ("fields",)

    def __init__(
        self,
        mapping: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__()

        self.fields: Dict[str, Field[Any]] = {}

        for key, value in (mapping or kwargs).items():
            self[key] = value

    def __setitem__(
        self,
        key: str,
        value: Any,
    ) -> None:
        if isinstance(value, Field):
            self.fields[key] = value

        super().__setitem__(key, value)


class StructureMeta(abc.ABCMeta):

    """
    Structure template metaclass.
    """

    __slots__ = ()

    _testplates_errors_: List[TestplatesError]
    _testplates_fields_: Mapping[str, Field[Any]]
    _testplates_codecs_: List[Codec[Any]]
    _testplates_default_codec_: Codec[Any]

    def __init__(
        cls,
        name: str,
        bases: Tuple[type, ...],
        attrs: StructureDict,
    ) -> None:
        super().__init__(name, bases, attrs)

        cls._testplates_errors_ = attrs.get(TESTPLATES_ERRORS_ATTR_NAME, [])
        cls._testplates_fields_ = attrs.fields
        cls._testplates_codecs_ = attrs.get(TESTPLATES_CODECS_ATTR_NAME, [])
        cls._testplates_default_codec_ = attrs.get(TESTPLATES_DEFAULT_CODEC_ATTR_NAME, None)

        for field in attrs.fields.values():
            cls._testplates_errors_.extend(field.errors)

    def __repr__(self) -> str:
        parameters = format_like_dict(self._testplates_fields_)

        return f"{testplates.__name__}.{type(self).__name__}({parameters})"

    @classmethod
    def __prepare__(
        mcs,
        __name: str,
        __bases: Tuple[type, ...],
        **kwargs: Any,
    ) -> StructureDict:
        return StructureDict()


class Structure(Mapping[str, Any], metaclass=StructureMeta):

    """
    Structure template base class.
    """

    __slots__ = ("_testplates_values_",)

    _testplates_errors_: ClassVar[List[TestplatesError]]
    _testplates_fields_: ClassVar[Mapping[str, Field[Any]]]
    _testplates_codecs_: ClassVar[List[Codec[Any]]]
    _testplates_default_codec_: ClassVar[Codec[Any]]

    def __init__(
        self,
        /,
        **values: Any,
    ) -> None:
        fields = self._testplates_fields_
        errors = self._testplates_errors_

        for key, value in values.items():
            if key not in fields.keys():
                errors.append(UnexpectedValueError(key, value))

        for key, field in fields.items():
            if not (result := field.validate(values.get(key, MISSING))):
                errors.append(unwrap_failure(result))

            if (default := field.default) is not MISSING:
                values.setdefault(key, default)

        self._testplates_values_: Mapping[str, Any] = values

    def __init_subclass__(cls, **kwargs: Any) -> None:
        pass

    def __repr__(self) -> str:
        return f"{type(self).__name__}({format_like_dict(self._testplates_values_)})"

    def __getitem__(self, item: str) -> object:
        return self._testplates_values_[item]

    def __iter__(self) -> Iterator[str]:
        return iter(self._testplates_values_)

    def __len__(self) -> int:
        return len(self._testplates_values_)

    def __eq__(self, other: Any) -> bool:
        for key, field in self._testplates_fields_.items():
            self_value: Maybe[Any] = self.get(key, MISSING)
            other_value: Maybe[Any] = other.get(key, MISSING)

            if not values_matches(self_value, other_value):
                return False

        return True
