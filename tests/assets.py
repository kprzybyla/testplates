__all__ = ["ObjectStorage", "MappingStorage", "StorageType", "TemplateType"]

from typing import Any, Type, TypeVar, Union, Dict

from testplates import Object, Mapping

_T = TypeVar("_T", covariant=True)

MappingStorage = dict


class ObjectStorage(Dict[str, _T]):
    def __getattr__(self, item: str) -> _T:
        try:
            return self[item]
        except KeyError:
            raise AttributeError(item) from None


StorageType = Type[Union[ObjectStorage[Any], Dict[str, Any]]]
TemplateType = Type[Union[Object, Mapping]]
