__all__ = ["ObjectStorage", "MappingStorage", "StorageType"]

from typing import Any, Type, TypeVar, Union, Dict

from testplates import ObjectTemplate, MappingTemplate

_T = TypeVar("_T", covariant=True)


class ObjectStorage(Dict[str, _T]):
    def __getattr__(self, item: str) -> _T:
        try:
            return self[item]
        except KeyError:
            raise AttributeError(item) from None


MappingStorage = dict

StorageType = Type[Union[ObjectStorage[Any], Dict[str, Any]]]
TemplateType = Type[Union[ObjectTemplate, MappingTemplate]]
