from __future__ import annotations

__all__ = ["Field", "Structure"]

import abc

from typing import (
    cast,
    overload,
    Any,
    Type,
    TypeVar,
    Generic,
    ClassVar,
    Dict,
    Union,
    Tuple,
    Optional,
)

from dataclasses import dataclass, field as dataclass_field

from .abc import Field as AbstractField, MissingType, Missing, Maybe, WILDCARD, ABSENT
from .exceptions import DanglingDescriptorError, MissingValueError, ProhibitedValueError

from .utils import compare

T = TypeVar("T")

Bases = Tuple[type, ...]


class Field(Generic[T], AbstractField[T]):

    __slots__ = ("_default", "_optional", "_name")

    def __init__(self, *, default: Maybe[T] = Missing, optional: bool = False) -> None:
        self._default = default
        self._optional = optional

        self._name: Optional[str] = None

    def __repr__(self) -> str:
        return f"Field[{self._name!r}, default={self._default!r}, is_optional={self._optional!r}]"

    def __set_name__(self, owner: Type[Structure[T]], name: str) -> None:
        self._name = name

    @overload
    def __get__(self, instance: None, owner: Type[Structure[T]]) -> Field[T]:
        ...

    @overload  # noqa: F811 (https://github.com/PyCQA/pyflakes/issues/320)
    def __get__(self, instance: Structure[T], owner: Type[Structure[T]]) -> T:
        ...

    def __get__(
        self, instance: Union[None, Structure[T]], owner: Type[Structure[T]]
    ) -> Union[Field[T], T]:  # noqa: F811
        if instance is None:
            return self

        value = instance._values_.get(self.name, Missing)

        if isinstance(value, MissingType):
            raise AttributeError(self._name)

        return value

    @property
    def name(self) -> str:
        if self._name is None:
            raise DanglingDescriptorError(self)

        return self._name

    @property
    def default(self) -> Maybe[T]:
        return self._default

    @property
    def is_optional(self) -> bool:
        return self._optional

    def validate(self, value: Maybe[T]) -> None:
        if value is Missing and self.default is Missing:
            raise MissingValueError(self)

        if (value is ABSENT or self.default is ABSENT) and not self.is_optional:
            raise ProhibitedValueError(self, value)

        if (value is WILDCARD or self.default is WILDCARD) and not self.is_optional:
            raise ProhibitedValueError(self, value)


@dataclass
class StructureDict(Generic[T], Dict[str, Any]):

    fields: Dict[str, Field[T]] = dataclass_field(default_factory=dict)

    def __setitem__(self, key: str, value: Any) -> None:
        if isinstance(value, Field):
            self.fields[key] = value

        super().__setitem__(key, value)


class StructureMeta(Generic[T], abc.ABCMeta):

    __slots__ = ()

    _fields_: Dict[str, Field[T]]

    @classmethod
    def __prepare__(mcs, __name: str, __bases: Bases, **kwargs: Any) -> StructureDict[T]:
        return StructureDict()

    def __repr__(self) -> str:
        return f"StructureMeta[{dict(self._fields_)}]"

    def __new__(mcs, name: str, bases: Bases, namespace: StructureDict[T]) -> StructureMeta[T]:
        instance = cast(StructureMeta[T], super().__new__(mcs, name, bases, namespace))
        instance._fields_ = namespace.fields

        return instance


class Structure(Generic[T], abc.ABC, metaclass=StructureMeta):

    __slots__ = ("_values_",)

    _fields_: ClassVar[Dict[str, Field[T]]]

    def __init__(self, **values: Maybe[T]) -> None:
        for key, field in self._fields_.items():
            field.validate(values.get(key, Missing))

        self._values_ = values

    def __eq__(self, other: Any) -> bool:
        for key, field in self._fields_.items():
            self_value = self._get_value_(self, key, default=field.default)
            other_value = self._get_value_(other, key)

            if not compare(self_value, other_value):
                return False

        return True

    @staticmethod
    @abc.abstractmethod
    def _get_value_(self: Any, key: str, *, default: Maybe[T] = Missing) -> Maybe[T]:
        raise NotImplementedError()

    def modify(self, **values: Maybe[T]) -> Structure[T]:
        modified_values = dict(self._values_)
        modified_values.update(values)

        return type(self)(**modified_values)
