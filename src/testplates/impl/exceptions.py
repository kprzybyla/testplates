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
]

from typing import Any


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

    def __init__(self, descriptor: Any) -> None:
        self.descriptor = descriptor

        super().__init__(f"Descriptor {descriptor!r} defined outside of the class definition")


class MissingValueError(TestplatesValueError):

    """
        Error indicating missing value.

        Raised when user forgets to set mandatory
        value for given field with actual value.
    """

    def __init__(self, field: Any) -> None:
        self.field = field

        super().__init__(f"Missing value for required field {field!r}")


class UnexpectedValueError(TestplatesValueError):

    """
        Error indicating unexpected value.

        Raised when user passes value which was
        not defined inside the template definition.
    """

    def __init__(self, key: str, value: Any) -> None:
        self.key = key
        self.value = value

        super().__init__(f"Unexpected key {key!r} with value {value!r}")


class ProhibitedValueError(TestplatesValueError):

    """
        Error indicating prohibited value.

        Raised when user sets prohibited value that
        is invalid for given field due to its nature.
    """

    def __init__(self, field: Any, value: Any) -> None:
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
