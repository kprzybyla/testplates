__all__ = ["ObjectStorage", "MappingStorage", "StorageType", "TemplateType"]

from typing import Type, TypeVar, Union, Dict

from testplates import Object, Mapping

_T = TypeVar("_T")


class ObjectStorage(Dict[str, _T]):
    def __getattr__(self, item: str) -> _T:
        try:
            return self[item]
        except KeyError:
            raise AttributeError(item) from None


class MappingStorage(Dict[str, _T]):
    pass


StorageType = Type[Union[ObjectStorage[_T], MappingStorage[_T]]]
TemplateType = Type[Union[Object[_T], Mapping[_T]]]
