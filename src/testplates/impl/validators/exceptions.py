__all__ = [
    "InvalidTypeValueError",
    "InvalidTypeError",
    "ProhibitedBoolValueError",
    "InvalidMinimumValueError",
    "InvalidMaximumValueError",
    "InvalidMinimumLengthError",
    "InvalidMaximumLengthError",
    "InvalidMinimumSizeError",
    "InvalidMaximumSizeError",
    "InvalidFormatError",
    "UniquenessError",
    "InvalidKeyError",
    "RequiredKeyMissingError",
    "MemberValidationError",
    "ItemValidationError",
    "FieldValidationError",
    "ChoiceValidationError",
]

from enum import Enum, EnumMeta
from typing import Any, AnyStr, TypeVar, Tuple, Sized, Pattern

from testplates.impl.base import TestplatesError

T = TypeVar("T")


class InvalidTypeValueError(TestplatesError):

    """
        Error indicating invalid type value.

        Raised when user passed value which is not a type
        or may not be used as the second argument of built-in
        isinstance() function (because it is not a classinfo).
    """

    def __init__(self, given_type: type) -> None:
        self.given_type = given_type

        super().__init__(f"Given value {given_type!r} is not a type nor a classinfo")


class InvalidTypeError(TestplatesError):

    """
        Error indicating invalid type.

        Raised when user passed a data which has a type
        not present in the specified allowed types tuple.
    """

    def __init__(self, data: Any, allowed_types: Tuple[type, ...]) -> None:
        self.data = data
        self.allowed_types = allowed_types

        super().__init__(
            f"Invalid type {type(data)!r} of data {data!r} (allowed types: {allowed_types!r})"
        )


class ProhibitedBoolValueError(TestplatesError):

    """
        Error indicating prohibited bool value.

        Raised when user passed a data which has a bool type
        but the validator does not allow bool type values.
    """

    def __init__(self, data: bool) -> None:
        self.data = data

        super().__init__(f"Prohibited type {bool!r} of data {data!r}")


class InvalidMinimumValueError(TestplatesError):

    """
        Error indicating invalid minimum value.

        Raised when user passed a data that does not match
        minimum value requirement specified by the validator.
    """

    def __init__(self, data: Any, minimum: Any) -> None:
        self.data = data
        self.minimum = minimum

        super().__init__(f"Invalid value {data!r} (minimum allowed value: {minimum!r})")


class InvalidMaximumValueError(TestplatesError):

    """
        Error indicating invalid maximum value.

        Raised when user passed a data that does not match
        maximum value requirement specified by the validator.
    """

    def __init__(self, data: Any, maximum: Any) -> None:
        self.data = data
        self.maximum = maximum

        super().__init__(f"Invalid value {data!r} (maximum allowed value: {maximum!r})")


class InvalidMinimumLengthError(TestplatesError):

    """
        Error indicating invalid minimum length.

        Raised when user passed a data that does not match
        minimum length requirement specified by the validator.
    """

    def __init__(self, data: Sized, minimum: Any) -> None:
        self.data = data
        self.minimum = minimum

        super().__init__(
            f"Invalid length {len(data)!r} of data {data!r} (minimum allowed length: {minimum!r})"
        )


class InvalidMaximumLengthError(TestplatesError):

    """
        Error indicating invalid maximum length.

        Raised when user passed a data that does not match
        maximum length requirement specified by the validator.
    """

    def __init__(self, data: Sized, maximum: Any) -> None:
        self.data = data
        self.maximum = maximum

        super().__init__(
            f"Invalid length {len(data)!r} of data {data!r} (maximum allowed length: {maximum!r})"
        )


class InvalidMinimumSizeError(TestplatesError):

    """
        Error indicating invalid minimum size.

        Raised when user passed a data that does not match
        minimum size requirement specified by the validator.
    """

    def __init__(self, data: Sized, minimum: Any) -> None:
        self.data = data
        self.minimum = minimum

        super().__init__(
            f"Invalid size {len(data)!r} of data {data!r} (minimum allowed size: {minimum!r})"
        )


class InvalidMaximumSizeError(TestplatesError):

    """
        Error indicating invalid maximum size.

        Raised when user passed a data that does not match
        maximum size requirement specified by the validator.
    """

    def __init__(self, data: Sized, maximum: Any) -> None:
        self.data = data
        self.maximum = maximum

        super().__init__(
            f"Invalid size {len(data)!r} of data {data!r} (maximum allowed size: {maximum!r})"
        )


class InvalidFormatError(TestplatesError):

    """
        Error indicating invalid data format.

        Raised when user passed a data that does not match
        the pattern requirement specified by the validator.
    """

    def __init__(self, data: AnyStr, regex: Pattern[AnyStr]) -> None:
        self.data = data
        self.regex = regex

        super().__init__(f"Invalid format of data {data!r} (allowed format: {regex!r})")


class UniquenessError(TestplatesError):

    """
        Error indicating not unique elements.

        Raised when user passed a data that contains
        not unique elements by the validator specified
        that all elements should be unique.
    """

    def __init__(self, data: Sized) -> None:
        self.data = data

        super().__init__(f"Data {data!r} does not contain unique elements")


class InvalidKeyError(TestplatesError):

    """
        Error indicating invalid key.

        Raised when user passed a data that contains
        key that was not expected by the validator.
    """

    def __init__(self, key: str, data: Any):
        self.key = key
        self.data = data

        super().__init__(f"Invalid key {key!r} found in data {data!r}")


class RequiredKeyMissingError(TestplatesError):

    """
        Error indicating required key missing.


        Raised when user passed a data that is missing
        a mandatory key specified by the validator.
    """

    def __init__(self, data: Any, key: str, field: Any) -> None:
        self.data = data
        self.key = key
        self.field = field

        super().__init__(f"Mandatory key {key!r} ({field!r}) missing in data {data!r}")


class MemberValidationError(TestplatesError):

    """
        Error indicating member validation failure.

        Raised when member validation fails with
        any kind of error. This exception wraps
        the enum, member and error information.
    """

    def __init__(self, enum_type: EnumMeta, member: Enum, error: TestplatesError) -> None:
        self.enum_type = enum_type
        self.member = member
        self.error = error

        super().__init__(f"Member {member!r} validation failure in {enum_type!r}: {error!r}")


class ItemValidationError(TestplatesError):

    """
        Error indicating item validation failure.

        Raised when item validation fails with
        any kind of error. This exception wraps
        the sequence, item and error information.
    """

    def __init__(self, data: Any, item: Any, error: TestplatesError) -> None:
        self.data = data
        self.item = item
        self.error = error

        super().__init__(f"Item {item!r} validation failure in {data!r}: {error!r}")


class FieldValidationError(TestplatesError):

    """
        Error indicating field validation failure.

        Raised when field validation fails with
        any kind of error. This exception wraps
        the mapping, field and error information.
    """

    def __init__(self, data: Any, field: Any, error: TestplatesError) -> None:
        self.data = data
        self.field = field
        self.error = error

        super().__init__(f"Field {field!r} validation failure in {data!r}: {error!r}")


class ChoiceValidationError(TestplatesError):

    """
        Error indicating choice validation failure.

        Raised when choice validation fails with
        any kind of error. This exception wraps
        the union, choice and error information.
    """

    def __init__(self, data: Any, error: TestplatesError):
        self.data = data
        self.error = error

        super().__init__(f"Choice TODO validation failure in {data!r}: {error!r}")