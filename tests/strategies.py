from typing import Any, TypeVar, Hashable, Callable

from hypothesis import strategies as st

_Ex = TypeVar("_Ex", covariant=True)

Draw = Callable[[st.SearchStrategy[_Ex]], _Ex]


def st_hashable() -> st.SearchStrategy[Hashable]:
    def filter_hashable(value: Any, /) -> bool:
        return isinstance(value, Hashable)

    return st.from_type(type).flatmap(st.from_type).filter(filter_hashable)


def st_anything_comparable() -> st.SearchStrategy[Any]:
    def filter_anything_comparable(value: Any, /) -> bool:
        return bool(value == value)

    return st.from_type(type).flatmap(st.from_type).filter(filter_anything_comparable)


def st_anything_except(*types: type) -> st.SearchStrategy[Any]:
    def filter_anything_except(value: Any, /) -> bool:
        return value == value and not isinstance(value, types)

    return st.from_type(type).flatmap(st.from_type).filter(filter_anything_except)


def st_anything_except_classinfo() -> st.SearchStrategy[Any]:
    def filter_anything_except_classinfo(value: Any, /) -> bool:
        try:
            isinstance(object, value)
        except TypeError:
            return bool(value == value)
        else:
            return False

    return st.from_type(type).flatmap(st.from_type).filter(filter_anything_except_classinfo)


def st_anytype_except_type_of(value: type, /) -> st.SearchStrategy[type]:
    def filter_anytype_except_type_of(typ: type, /) -> bool:
        return not issubclass(type(value), typ)

    return st.from_type(type).flatmap(st.from_type).map(type).filter(filter_anytype_except_type_of)
