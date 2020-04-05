__all__ = [
    "TestplatesError",
    "TestplatesValueError",
    "DanglingDescriptorError",
    "MissingValueError",
    "UnexpectedValueError",
    "ProhibitedValueError",
    "MissingBoundaryError",
    "InvalidLengthValueError",
    "MutuallyExclusiveBoundariesError",
    "OverlappingBoundariesError",
    "SingleMatchBoundariesError",
    "TooLittleValuesError",
    "InternalError",
    "MissingValueInternalError",
    "UnreachableCodeError",
]

from typing import Any, TypeVar, Optional

from testplates import abc

_T = TypeVar("_T")


class TestplatesError(Exception):

    """
        Base testplates error.
    """


class TestplatesValueError(ValueError, TestplatesError):

    """
        Base testplates value error.
    """


class DanglingDescriptorError(TestplatesError):

    """
        Error indicating dangling descriptor.

        Raised when user defined descriptor not
        as class variable. Such definition does
        not trigger descriptor protocol and may
        cause unexpected behaviour.
    """

    def __init__(self, descriptor: abc.Descriptor[Any, _T]) -> None:
        super().__init__(f"Descriptor {descriptor!r} is not attached to any class")


class MissingValueError(TestplatesValueError):

    """
        Error indicating missing value.

        Raised when user forgot to set mandatory
        value for given field with actual value.
    """

    def __init__(self, field: abc.Descriptor[Any, _T]) -> None:
        super().__init__(f"Missing value in required field {field!r}")


class UnexpectedValueError(TestplatesValueError):

    """
        Error indicating unexpected value.

        Raised when user passed value which was
        not defined inside the template class.
    """

    def __init__(self, key: str, value: _T) -> None:
        super().__init__(f"Unexpected key {key!r} with value {value!r}")


class ProhibitedValueError(TestplatesValueError):

    """
        Error indicating prohibited value.

        Raised when user set prohibited value that
        is invalid for given field due to its nature.
    """

    def __init__(self, field: abc.Descriptor[Any, _T], value: Any) -> None:
        super().__init__(f"Value {value!r} is prohibited for field {field!r}")


class MissingBoundaryError(TestplatesValueError):

    """
        Error indicating missing boundary.

        Raised when user forgot to set mandatory boundary
        for given field with minimum and maximum constraints.
    """

    def __init__(self, name: str) -> None:
        super().__init__(f"Missing value for mandatory boundary {name!r}")


class InvalidLengthValueError(TestplatesValueError):

    """
        Error indicating invalid length boundary value.

        Raised when user sets boundary with value that
        does not meet length boundary value expectations.
    """

    def __init__(self, value: Optional[int]) -> None:
        super().__init__(f"Invalid value {value} ...")


class MutuallyExclusiveBoundariesError(TestplatesValueError):

    """
        Error indicating exclusive and inclusive boundaries collision.

        Raised when user set both same exclusive
        and inclusive value for given constraint.
    """

    def __init__(self, name: str) -> None:
        super().__init__(f"Exclusive and inclusive {name} boundaries are mutually exclusive")


class OverlappingBoundariesError(TestplatesValueError):

    """
        ...
    """


class SingleMatchBoundariesError(TestplatesValueError):

    """
        ...
    """


class TooLittleValuesError(TestplatesValueError):

    """
        Error indicating that not enough values were provided.

        Raised when user passes zero values for template
        that requires at least one value to be provided.
    """

    def __init__(self, required: int) -> None:
        super().__init__(f"Template requires at least {required} value(s) to be provided")


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

    def __init__(self, field: abc.Descriptor[Any, _T]) -> None:
        super().__init__(f"Field {field.name!r} is internally missing value ({field!r})")


class UnreachableCodeError(InternalError):

    """
        ...
    """

    def __init__(self) -> None:
        super().__init__("This code section should be unreachable")
