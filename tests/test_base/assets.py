__all__ = ["CreateFunctionType", "StorageType", "ObjectStorage", "MappingStorage"]

from typing import Any, Union, Dict, Protocol

from testplates import CreateObjectFunctionType, CreateMappingFunctionType

CreateFunctionType = Union[CreateObjectFunctionType, CreateMappingFunctionType]


class StorageType(Protocol):
    def __call__(self, **values: Any) -> None:
        ...

    def __eq__(self, other: Any) -> bool:
        ...


class ObjectStorage:
    def __init__(self, **values: Any) -> None:
        for key, value in values.items():
            setattr(self, key, value)


class MappingStorage(Dict[str, Any]):
    pass
