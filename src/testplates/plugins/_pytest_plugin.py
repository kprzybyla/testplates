from typing import Any, TypeVar, Iterable, Optional

from testplates import Object, Mapping
from testplates.value import MISSING

_T = TypeVar("_T")

SPACE = " "
INDENT = "    "
NEWLINE = "\n"

EQUAL_INDICATOR = "~"
UNEQUAL_INDICATOR = "!"
MISSING_INDICATOR = "-"
EXTRA_INDICATOR = "+"

EQUAL_SIGN = "~"
UNEQUAL_SIGN = "!"


def is_equality(operation: str) -> bool:
    return operation in ["==", "!="]


def equal_value(key: str, self_value: Any, other_value: Any, *, level: int = 0) -> Iterable[str]:
    yield EQUAL_INDICATOR
    yield INDENT * level
    yield key
    yield ":"
    yield SPACE
    yield repr(self_value)
    yield SPACE
    yield "("
    yield str(type(self_value))
    yield ")"
    yield SPACE
    yield ":"
    yield SPACE
    yield repr(other_value)
    yield SPACE
    yield "("
    yield str(type(other_value))
    yield ")"


def unequal_value(key: str, self_value: Any, other_value: Any, *, level: int = 0) -> Iterable[str]:
    yield UNEQUAL_INDICATOR
    yield INDENT * level
    yield key
    yield ":"
    yield SPACE
    yield repr(self_value)
    yield SPACE
    yield "("
    yield str(type(self_value))
    yield ")"
    yield SPACE
    yield ":"
    yield SPACE
    yield repr(other_value)
    yield SPACE
    yield "("
    yield str(type(other_value))
    yield ")"


def missing_value(key: str, self_value: Any, *, level: int = 0) -> Iterable[str]:
    yield MISSING_INDICATOR
    yield INDENT * level
    yield key
    yield ":"
    yield SPACE
    yield repr(self_value)
    yield SPACE
    yield "("
    yield str(type(self_value))
    yield ")"


def assertrepr_compare_object(self: Object[_T], other: Any) -> Iterable[str]:
    yield str(self)
    yield "vs"
    yield str(other)
    yield NEWLINE
    yield type(self).__name__
    yield SPACE
    yield "{"
    yield NEWLINE

    for key, field in self._fields_.items():
        self_value = self._get_value_(self, key)
        other_value = self._get_value_(other, key)

        if other_value is MISSING:
            yield from missing_value(key, self_value, level=1)
        elif self_value != other_value:
            yield from unequal_value(key, self_value, other_value, level=1)
        else:
            yield from equal_value(key, self_value, other_value, level=1)

        yield NEWLINE

    yield "}"


def assertrepr_compare_mapping(self_value: Mapping[_T], other_value: Any) -> Iterable[str]:
    yield "TODO"


def pytest_assertrepr_compare(op: str, left: Any, right: Any) -> Optional[Iterable[str]]:
    if not is_equality(op):
        return None

    if isinstance(left, Object):
        return "".join((assertrepr_compare_object(left, right))).split(NEWLINE)

    if isinstance(right, Object):
        return "".join(assertrepr_compare_object(right, left)).split(NEWLINE)

    if isinstance(left, Mapping):
        return list(assertrepr_compare_mapping(left, right))

    if isinstance(right, Mapping):
        return list(assertrepr_compare_mapping(right, left))
