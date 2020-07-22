from __future__ import annotations

__all__ = ["Field", "StructureMeta", "Structure"]

import abc

from typing import (
    cast,
    overload,
    Any,
    TypeVar,
    Generic,
    ClassVar,
    Union,
    Tuple,
    Dict,
    Callable,
    Optional,
)

import testplates

from testplates.impl.utils import format_like_dict
from testplates.impl.exceptions import (
    DanglingDescriptorError,
    MissingValueError,
    UnexpectedValueError,
    ProhibitedValueError,
)

from .result import Result, Failure
from .value import is_value, values_matches, Maybe, ANY, WILDCARD, ABSENT, MISSING

T = TypeVar("T", covariant=True)
V = TypeVar("V")

Validator = Callable[[Any], Result[None, Exception]]


class Field(Generic[T]):

    """
        Field descriptor class.
    """

    __slots__ = ("_validator", "_default", "_default_factory", "_optional", "_name")

    def __init__(
        self,
        validator: Validator,
        /,
        *,
        default: Maybe[T] = MISSING,
        default_factory: Maybe[Callable[[], T]],
        optional: bool = False,
    ) -> None:
        self._validator = validator
        self._default = default
        self._default_factory = default_factory
        self._optional = optional

        self._name: Optional[str] = None

    def __repr__(self) -> str:
        parameters = [f"{self._name!r}"]

        if (default := self.default) is not MISSING:
            parameters.append(f"default={default!r}")

        parameters.append(f"optional={self.is_optional!r}")

        return f"{testplates.__name__}.{type(self).__name__}({', '.join(parameters)})"

    def __set_name__(self, owner: StructureMeta[T], name: str) -> None:
        self._name = name

    @overload
    def __get__(self, instance: None, owner: StructureMeta[T]) -> Field[T]:
        ...

    @overload
    def __get__(self, instance: Structure[T], owner: StructureMeta[T]) -> T:
        ...

    # noinspection PyProtectedMember
    def __get__(
        self, instance: Optional[Structure[T]], owner: StructureMeta[T]
    ) -> Union[Field[T], T]:

        """
            Returns either field itself or field value.

            Return value depends on the fact whether field was accessed
            via :class:`Structure` class object or class instance attribute.

            :param instance: :class:`Structure` class instance to which field is attached or None
            :param owner: :class:`Structure` class object to which field is attached
        """

        if instance is None:
            return self

        return instance._values_[self.name]

    @property
    def name(self) -> str:
        if self._name is None:
            raise DanglingDescriptorError(self)

        return self._name

    @property
    def validator(self) -> Validator:

        """
            Returns field validator function.
        """

        return self._validator

    @property
    def default(self) -> Maybe[T]:

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
    def validate(self, value: Maybe[T], /) -> None:

        """
            Validates the given value against the field requirements.

            :param value: value to be validated
        """

        default = self.default

        if value is ANY:
            pass

        elif value is MISSING and default is MISSING:
            raise MissingValueError(self)

        elif (value is ABSENT or default is ABSENT) and not self.is_optional:
            raise ProhibitedValueError(self, value)

        elif (value is WILDCARD or default is WILDCARD) and not self.is_optional:
            raise ProhibitedValueError(self, value)

        elif is_value(value) and (result := self.validator(value)).is_failure:
            raise Failure.get_error(result)


class StructureDict(Generic[T, V], Dict[str, V]):

    __slots__ = ("fields",)

    def __init__(self, **kwargs: V) -> None:
        super().__init__(**kwargs)

        self.fields: Dict[str, Field[T]] = {}

    def __setitem__(self, key: str, value: V) -> None:
        if isinstance(value, Field):
            self.fields[key] = value

        super().__setitem__(key, value)


class StructureMeta(Generic[T], abc.ABCMeta):

    """
        Structure template metaclass.
    """

    __slots__ = ()

    _fields_: Dict[str, Field[T]]

    @classmethod
    def __prepare__(
        mcs, __name: str, __bases: Tuple[type, ...], **kwargs: Any
    ) -> StructureDict[T, Any]:
        return StructureDict()

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{type(self).__name__}({format_like_dict(self._fields_)})"

    def __new__(
        mcs, name: str, bases: Tuple[type, ...], namespace: StructureDict[T, Any]
    ) -> StructureMeta[T]:
        instance = cast(StructureMeta[T], super().__new__(mcs, name, bases, namespace))
        instance._fields_ = namespace.fields

        return instance

    def _create_(cls, name: str, fields: Dict[str, Field[T]] = None) -> StructureMeta[T]:
        bases = (cls,)
        fields = fields or {}

        metaclass = cls.__class__
        namespace = metaclass.__prepare__(name, bases)

        instance = metaclass.__new__(metaclass, name, bases, namespace)
        instance._fields_ = fields

        for name, field in fields.items():
            field.__set_name__(instance, name)

        return instance


class Structure(Generic[T], abc.ABC, metaclass=StructureMeta):

    """
        Structure template base class.
    """

    __slots__ = ("_values_",)

    _fields_: ClassVar[Dict[str, Field[T]]]

    def __init__(self, **values: T) -> None:
        keys = self._fields_.keys()

        for key, value in values.items():
            if key not in keys:
                raise UnexpectedValueError(key, value)

        for key, field in self._fields_.items():
            field.validate(values.get(key, MISSING))

            if field.default is not MISSING:
                values.setdefault(key, field.default)

        self._values_ = values

    def __repr__(self) -> str:
        return f"{type(self).__name__}({format_like_dict(self._values_)})"

    def __eq__(self, other: Any) -> bool:
        for key, field in self._fields_.items():
            self_value = self._get_value_(self, key)
            other_value = self._get_value_(other, key)

            if not values_matches(self_value, other_value):
                return False

        return True

    @staticmethod
    @abc.abstractmethod
    def _get_value_(self: Any, key: str, /, *, default: Maybe[T] = MISSING) -> Maybe[T]:

        """
            Extracts value by given key using a type specific protocol.

            If value is missing, returns default value.

            :param self: object with a type specific protocol
            :param key: key used to access the value in a structure
            :param default: default value that will be used in case value is missing
        """
