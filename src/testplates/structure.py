from __future__ import annotations

__all__ = ["Field", "StructureMeta", "Structure"]

import abc

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
    Dict,
    Optional,
)

from .abc import Descriptor
from .utils import matches
from .value import WILDCARD, ABSENT, MISSING, Maybe

from .exceptions import (
    DanglingDescriptorError,
    MissingValueError,
    UnexpectedValueError,
    ProhibitedValueError,
    MissingValueInternalError,
)

_T = TypeVar("_T", covariant=True)

Bases = Tuple[type, ...]

# TODO(kprzybyla): Remove noqa (F811) after github.com/PyCQA/pyflakes/issues/320 is delivered


class Field(Generic[_T], Descriptor[_T]):

    __slots__ = ("_default", "_optional", "_name")

    def __init__(self, *, default: Maybe[_T] = MISSING, optional: bool = False) -> None:
        self._default = default
        self._optional = optional

        self._name: Optional[str] = None

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}"
            f"[{self._name!r}, default={self.default!r}, is_optional={self.is_optional!r}]"
        )

    def __set_name__(self, owner: Type[Structure[_T]], name: str) -> None:
        self._name = name

    @overload
    def __get__(self, instance: None, owner: Type[Structure[_T]]) -> Field[_T]:

        """
            Returns field itself when field is accessed
            via :class:`Structure` class object attribute.

            :param instance: None
            :param owner: :class:`Structure` class object to which field is attached
        """

    @overload  # noqa
    def __get__(self, instance: Structure[_T], owner: Type[Structure[_T]]) -> _T:

        """
            Returns field value when field is accessed
            via :class:`Structure` class instance attribute.

            :param instance: :class:`Structure` class instance to which field is attached
            :param owner: :class:`Structure` class object to which field is attached
        """

    def __get__(
        self, instance: Optional[Structure[_T]], owner: Type[Structure[_T]]
    ) -> Union[Field[_T], _T]:  # noqa

        """
            Returns either field itself or field value.

            Return value depends on the fact whether field was access
            via :class:`Structure` class object or class instance attribute.

            :param instance: :class:`Structure` class instance to which field is attached or None
            :param owner: :class:`Structure` class object to which field is attached

            :raises AttributeError: When field value is missing when trying to access it
        """

        if instance is None:
            return self

        value: Maybe[_T] = instance._values_.get(self.name, MISSING)

        if value is MISSING:
            raise MissingValueInternalError(self)  # pragma: no cover

        return value

    @property
    def name(self) -> str:
        if self._name is None:
            raise DanglingDescriptorError(self)

        return self._name

    @property
    def default(self) -> Maybe[_T]:

        """
            Returns field default value.

            If the field does not have a default value,
            missing value indicator is returned instead.
        """

        return self._default

    @property
    def is_optional(self) -> bool:

        """
            Returns True if field is optional, otherwise False.
        """

        return self._optional

    def validate(self, value: Maybe[_T]) -> None:

        """
            Validates the given value against the field.

            :param value: value to be validated
        """

        if value is MISSING and self.default is MISSING:
            raise MissingValueError(self)

        if (value is ABSENT or self.default is ABSENT) and not self.is_optional:
            raise ProhibitedValueError(self, value)

        if (value is WILDCARD or self.default is WILDCARD) and not self.is_optional:
            raise ProhibitedValueError(self, value)


class _StructureDict(Generic[_T], Dict[str, Any]):

    __slots__ = ("_fields_",)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self._fields_: Dict[str, Field[_T]] = {}

    def __setitem__(self, key: str, value: Any) -> None:
        if isinstance(value, Field):
            self.fields[key] = value

        super().__setitem__(key, value)

    @property
    def fields(self) -> Dict[str, Field[_T]]:

        """
            Returns fields descriptors.
        """

        return self._fields_


class StructureMeta(Generic[_T], abc.ABCMeta):

    __slots__ = ()

    _fields_: Dict[str, Field[_T]]

    @classmethod
    def __prepare__(mcs, __name: str, __bases: Bases, **kwargs: Any) -> _StructureDict[_T]:
        return _StructureDict()

    def __repr__(self) -> str:
        return f"StructureMeta[{dict(self._fields_)}]"

    def __new__(mcs, name: str, bases: Bases, namespace: _StructureDict[_T]) -> StructureMeta[_T]:
        instance = cast(StructureMeta[_T], super().__new__(mcs, name, bases, namespace))
        instance._fields_ = namespace.fields

        return instance


class Structure(Generic[_T], abc.ABC, metaclass=StructureMeta):

    __slots__ = ("_values_",)

    _fields_: ClassVar[Dict[str, Field[_T]]]

    def __init__(self, **values: _T) -> None:
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
        return f"{type(self).__name__}[{self._values_}]"

    def __eq__(self, other: Any) -> bool:
        for key, field in self._fields_.items():
            self_value = self._get_value_(self, key)
            other_value = self._get_value_(other, key)

            if not matches(self_value, other_value):
                return False

        return True

    @staticmethod
    @abc.abstractmethod
    def _get_value_(self: Any, key: str, *, default: Maybe[_T] = MISSING) -> Maybe[_T]:

        """
            Extracts value by given key using a specific protocol.

            If value is missing, returns default value.

            :param self: object with a specific protocol
            :param key: key used to access the value
            :param default: default value in case value is missing
        """
