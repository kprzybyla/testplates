__all__ = [
    "TestplatesError",
    "DanglingDescriptorError",
    "MissingValueError",
    "UnexpectedValueError",
    "ProhibitedValueError",
    "ExclusiveInclusiveValueError",
]

from typing import TypeVar

from . import abc
from .value import Maybe

T = TypeVar("T")


class TestplatesError(Exception):

    """
        Base testplates error.
    """


class DanglingDescriptorError(TestplatesError):

    """
        Error indicating dangling descriptor.

        Raised when user defined descriptor not
        as class variable. Such definition does
        not trigger descriptor protocol and may
        cause unexpected behaviour.
    """

    def __init__(self, descriptor: abc.Descriptor[T]) -> None:
        super().__init__(f"Descriptor {descriptor!r} is not attached to any class")


class MissingValueError(ValueError, TestplatesError):

    """
        Error indicating missing value.

        Raised when user forgot to set mandatory
        value for given field with actual value.
    """

    def __init__(self, field: abc.Descriptor[T]) -> None:
        super().__init__(f"Missing value in required field {field.name!r} ({field!r})")


class UnexpectedValueError(ValueError, TestplatesError):

    """
        Error indicating unexpected value.

        Raised when user passed value which was
        not defined inside the template class.
    """

    def __init__(self, key: str, value: Maybe[T]) -> None:
        super().__init__(f"Unexpected key {key!r} with value {value!r}")


class ProhibitedValueError(ValueError, TestplatesError):

    """
        Error indicating prohibited value.

        Raised when user set prohibited value that
        is invalid for given field due to its nature.
    """

    def __init__(self, field: abc.Descriptor[T], value: Maybe[T]) -> None:
        super().__init__(f"Value {value} is prohibited for field {field.name!r} ({field!r}")


class MutuallyExclusiveBoundaryError(ValueError, TestplatesError):

    """
        Error indicating exclusive and inclusive boundaries collision.

        Raised when user set both same exclusive
        and inclusive value for given constraint.
    """

    def __init__(self) -> None:
        super().__init__(f"Exclusive and inclusive boundaries are mutually exclusive")


class InternalError(TestplatesError):

    """
        Error indicating internal error inside testplates library.

        Raised when upon any kind of illegal
        behaviour inside testplates library.
    """

    def __init__(self, message: str) -> None:
        super().__init__(f"[InternalError] {message}")


class MissingValueInternalError(InternalError):

    """
        Error indicating missing value internal error.

        Raised when internally value is missing but
        from logical point of view it should not.
    """

    def __init__(self, field: abc.Descriptor[T]):
        super().__init__(f"Field {field.name!r} is internally missing value ({field!r})")
