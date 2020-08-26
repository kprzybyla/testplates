from __future__ import annotations

__all__ = (
    "Field",
    "Structure",
    "StructureMeta",
)

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
    Mapping,
    Callable,
    Optional,
)

from resultful import (
    success,
    failure,
    Result,
)

import testplates

from testplates.impl.utils import format_like_dict

from .value import (
    is_value,
    values_matches,
    Value,
    Maybe,
    Validator,
    ANY,
    WILDCARD,
    ABSENT,
    MISSING,
)

from .exceptions import (
    TestplatesError,
    MissingValueError,
    UnexpectedValueError,
    ProhibitedValueError,
)

_T = TypeVar("_T", covariant=True)


class Field(Generic[_T]):

    """
    Field descriptor class.
    """

    __slots__ = (
        "_validator",
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
        default: Maybe[_T] = MISSING,
        default_factory: Maybe[Callable[[], _T]] = MISSING,
        optional: bool = False,
    ) -> None:
        self._validator = validator
        self._default = default
        self._default_factory = default_factory
        self._optional = optional

    def __repr__(self) -> str:
        parameters = [f"{self._name!r}"]

        if (default := self.default) is not MISSING:
            parameters.append(f"default={default!r}")

        parameters.append(f"optional={self.is_optional!r}")

        return f"{testplates.__name__}.{type(self).__name__}({', '.join(parameters)})"

    def __set_name__(self, owner: Callable[..., Structure], name: str) -> None:
        self._name = name

    @overload
    def __get__(self, instance: None, owner: Callable[..., Structure]) -> Field[_T]:
        ...

    @overload
    def __get__(self, instance: Structure, owner: Callable[..., Structure]) -> Value[_T]:
        ...

    # noinspection PyProtectedMember
    def __get__(
        self,
        instance: Optional[Structure],
        owner: Callable[..., Structure],
    ) -> Union[Field[_T], Value[_T]]:

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

        """
        Returns field name.
        """

        return self._name

    @property
    def validator(self) -> Validator:

        """
        Returns field validator function.
        """

        return self._validator

    # noinspection PyCallingNonCallable
    @property
    def default(self) -> Maybe[_T]:

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
    def validate(self, value: Maybe[Value[_T]], /) -> Result[None, TestplatesError]:

        """
        Validates the given value against the field requirements.

        :param value: value to be validated
        """

        default = self.default

        if value is ANY:
            return success(None)

        elif value is MISSING and default is MISSING:
            return failure(MissingValueError(self))

        elif (value is ABSENT or default is ABSENT) and not self.is_optional:
            return failure(ProhibitedValueError(self, value))

        elif (value is WILDCARD or default is WILDCARD) and not self.is_optional:
            return failure(ProhibitedValueError(self, value))

        elif is_value(value) and not (result := self.validator(value)):
            return result

        return success(None)


class StructureDict(Dict[str, Any]):

    __slots__ = ("fields",)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.fields: Dict[str, Field[Any]] = {}

    def __setitem__(self, key: str, value: Any) -> None:
        if isinstance(value, Field):
            self.fields[key] = value

        super().__setitem__(key, value)


class StructureMeta(abc.ABCMeta):

    """
    Structure template metaclass.
    """

    __slots__ = ()

    _fields_: Mapping[str, Field[Any]]

    def __init__(cls, name: str, bases: Tuple[type, ...], attrs: StructureDict) -> None:
        super().__init__(name, bases, attrs)

        cls._fields_ = attrs.fields

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{type(self).__name__}({format_like_dict(self._fields_)})"

    @classmethod
    def __prepare__(mcs, __name: str, __bases: Tuple[type, ...], **kwargs: Any) -> StructureDict:
        return StructureDict()

    # noinspection PyTypeChecker
    # noinspection PyArgumentList
    def _create_(cls, name: str, **fields: Field[Any]) -> StructureMeta:
        bases = (cls,)
        metaclass = cls.__class__

        attrs = metaclass.__prepare__(name, bases)

        for key, field in (fields or {}).items():
            attrs.__setitem__(key, field)

        instance = cast(StructureMeta, metaclass.__new__(metaclass, name, bases, attrs))
        metaclass.__init__(instance, name, bases, attrs)

        return instance


class Structure(abc.ABC, metaclass=StructureMeta):

    """
    Structure template base class.
    """

    __slots__ = ("_values_",)

    # noinspection PyTypeHints
    # noinspection PyTypeChecker
    _Self_ = TypeVar("_Self_", bound="Structure")

    _fields_: ClassVar[Mapping[str, Field[Any]]]

    def __init__(self) -> None:
        self._values_: Mapping[str, Value[Any]] = {}

    def __repr__(self) -> str:
        return f"{type(self).__name__}({format_like_dict(self._values_)})"

    def __eq__(self, other: Any) -> bool:
        for key, field in self._fields_.items():
            self_value: Maybe[Value[Any]] = self._get_value_(self, key)
            other_value: Maybe[Value[Any]] = self._get_value_(other, key)

            if not values_matches(self_value, other_value):
                return False

        return True

    def _init_(self: _Self_, **values: Value[Any]) -> Result[_Self_, TestplatesError]:
        keys = self._fields_.keys()

        for key, value in values.items():
            if key not in keys:
                return failure(UnexpectedValueError(key, value))

        for key, field in self._fields_.items():
            if not (result := field.validate(values.get(key, MISSING))):
                return result

            if field.default is not MISSING:
                values.setdefault(key, field.default)

        self._values_ = values

        return success(self)

    @staticmethod
    @abc.abstractmethod
    def _get_value_(self: Any, key: str, /, *, default: Maybe[_T] = MISSING) -> Maybe[Value[_T]]:

        """
        Extracts value by given key using a type specific protocol.

        If value is missing, returns default value.

        :param self: object with a type specific protocol
        :param key: key used to access the value in a structure
        :param default: default value that will be used in case value is missing
        """
