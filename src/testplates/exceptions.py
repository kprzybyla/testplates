__all__ = [
    "TestplatesError",
    "TestplatesValueError",
    "DanglingDescriptorError",
    "MissingValueError",
    "UnexpectedValueError",
    "ProhibitedValueError",
    "MissingBoundaryError",
    "InvalidLengthError",
    "MutuallyExclusiveBoundariesError",
    "OverlappingBoundariesError",
    "SingleMatchBoundariesError",
    "InsufficientValuesError",
    "InternalError",
    "MissingValueInternalError",
    "UnreachableCodeExecutionInternalError",
]

from typing import Any, TypeVar, Generic, Final

from testplates import abc

_C = TypeVar("_C")
_T = TypeVar("_T")

ISSUE_TRACKER: Final[str] = "https://github.com/kprzybyla/testplates/issues"


class TestplatesError(Exception):

    """
        Base testplates error.
    """

    def __init__(self, message: str):
        super().__init__(message)

    @property
    def message(self) -> str:

        """
            Returns error message.
        """

        return "".join(self.args)


class TestplatesValueError(ValueError, TestplatesError):

    """
        Base testplates value error.
    """


class DanglingDescriptorError(TestplatesError):

    """
        Error indicating dangling descriptor.

        Raised when user defines descriptor outside of the class
        definition. Such declaration does not trigger descriptor
        protocol and may cause unexpected behaviour.
    """

    def __init__(self, descriptor: abc.Descriptor[_C, _T]) -> None:
        self.descriptor = descriptor

        super().__init__(f"Descriptor {descriptor!r} defined outside of the class definition")


class MissingValueError(TestplatesValueError):

    """
        Error indicating missing value.

        Raised when user forgets to set mandatory
        value for given field with actual value.
    """

    def __init__(self, field: abc.Descriptor[_C, _T]) -> None:
        self.field = field

        super().__init__(f"Missing value for required field {field!r}")


class UnexpectedValueError(TestplatesValueError):

    """
        Error indicating unexpected value.

        Raised when user passes value which was
        not defined inside the template definition.
    """

    def __init__(self, key: str, value: _T) -> None:
        self.key = key
        self.value = value

        super().__init__(f"Unexpected key {key!r} with value {value!r}")


class ProhibitedValueError(TestplatesValueError):

    """
        Error indicating prohibited value.

        Raised when user sets prohibited value that
        is invalid for given field due to its nature.
    """

    def __init__(self, field: abc.Descriptor[_C, _T], value: Any) -> None:
        self.field = field
        self.value = value

        super().__init__(f"Prohibited value {value!r} for field {field!r}")


class MissingBoundaryError(TestplatesValueError):

    """
        Error indicating missing boundary.

        Raised when user forgets to set mandatory boundary
        for given template with minimum and maximum constraints.
    """

    def __init__(self, name: str) -> None:
        self.name = name

        super().__init__(f"Missing value for mandatory boundary {self.name!r}")


class InvalidLengthError(TestplatesValueError):

    """
        Error indicating invalid length boundary value.

        Raised when user sets length boundary with value
        that does not meet length boundary requirements.
    """

    def __init__(self, boundary: Any) -> None:
        self.boundary = boundary

        super().__init__(f"Invalid value for length boundary {boundary!r}")


class MutuallyExclusiveBoundariesError(TestplatesValueError):

    """
        Error indicating exclusive and inclusive boundaries collision.

        Raised when user sets mutually exclusive
        boundaries at the same time with value.
    """

    def __init__(self, name: str) -> None:
        self.name = name

        super().__init__(f"Mutually exclusive {name!r} boundaries set at the same time")


class OverlappingBoundariesError(TestplatesValueError):

    """
        Error indicating overlapping boundaries.

        Raised when user sets both minimum and maximum
        boundaries with values the overlap over each other.
    """

    def __init__(self, minimum: Any, maximum: Any) -> None:
        self.minimum = minimum
        self.maximum = maximum

        super().__init__(f"Overlapping minimum {minimum!r} and maximum {maximum!r} boundaries")


class SingleMatchBoundariesError(TestplatesValueError):

    """
        Error indicating single match boundaries range.

        Raised when user sets boundaries with values that
        creates range which matches only single value.
    """

    def __init__(self, minimum: Any, maximum: Any) -> None:
        self.minimum = minimum
        self.maximum = maximum

        super().__init__(f"Single match minimum {minimum!r} and maximum {maximum!r} boundaries")


class InsufficientValuesError(TestplatesValueError):

    """
        Error indicating insufficient amount of values.

        Raised when user passes not enough values for template
        that accepts infinite number of values but requires at
        least a specific number of values to be provided.
    """

    def __init__(self, required: int) -> None:
        self.required = required

        super().__init__(f"Expected at least {required!r} value(s) to be provided")


class InternalError(TestplatesError):

    """
        Error indicating internal error.

        Raised upon any kind of illegal behaviour.
        Indicates a bug to be reported via issue tracker.
    """

    def __init__(self, message: str) -> None:
        super().__init__(f"{message}\n\nPlease report a bug on {ISSUE_TRACKER}")


class MissingValueInternalError(InternalError):

    """
        Error indicating missing value internal error.

        Raised when internally value is missing but
        from logical point of view it should not be.
    """

    def __init__(self, field: abc.Descriptor[_C, _T]) -> None:
        self.field = field

        super().__init__(f"Missing value for field {field!r}")


class UnreachableCodeExecutionInternalError(InternalError):

    """
        Error indicating unreachable code being executed.

        Raised when code section that should never be reached was executed.
    """

    def __init__(self) -> None:
        super().__init__("Unreachable code section reached")
