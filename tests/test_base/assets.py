from typing import (
    Any,
    TypeVar,
    Union,
    Dict,
    Protocol,
)

from testplates import (
    CreateObjectFunctionType,
    CreateMappingFunctionType,
)

_T = TypeVar("_T")

CreateFunctionType = Union[CreateObjectFunctionType, CreateMappingFunctionType]


class StorageType(Protocol):
    def __call__(self: _T, **values: Any) -> _T:
        ...

    def __eq__(self, other: Any) -> bool:
        ...


class ObjectStorage:
    def __init__(self, **values: Any) -> None:
        for key, value in values.items():
            setattr(self, key, value)


class MappingStorage(Dict[str, Any]):
    pass
