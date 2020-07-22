__all__ = [
    "ValidationError",
    "InvalidTypeValueError",
    "InvalidTypeError",
    "ProhibitedBooleanValueError",
    "InvalidMinimumValueError",
    "InvalidMaximumValueError",
    "InvalidMinimumLengthError",
    "InvalidMaximumLengthError",
    "InvalidPatternTypeError",
    "InvalidFormatError",
    "ItemValidationError",
    "InvalidMinimumSizeError",
    "InvalidMaximumSizeError",
    "UniquenessError",
    "MemberValidationError",
    "FieldValidationError",
    "RequiredKeyMissingError",
    "InvalidKeyError",
    "ChoiceValidationError",
]

from enum import Enum, EnumMeta
from typing import Any, AnyStr, Union, Tuple, Sized, Pattern

from testplates.impl.base import TestplatesError, TestplatesValueError


class ValidationError(TestplatesValueError):
    pass


class InvalidTypeValueError(ValidationError):
    def __init__(self, given_type: type) -> None:
        self.given_type = given_type

        super().__init__("TODO...")


class InvalidTypeError(ValidationError):
    def __init__(self, data: Any, allowed_types: Tuple[type, ...]) -> None:
        self.data = data
        self.allowed_types = allowed_types

        super().__init__("TODO...")


class ProhibitedBooleanValueError(ValidationError):
    def __init__(self, data: bool) -> None:
        self.data = data

        super().__init__("TODO...")


class InvalidMinimumValueError(ValidationError):
    def __init__(self, data: Any, minimum: Any) -> None:
        self.data = data
        self.minimum = minimum

        super().__init__("TODO...")


class InvalidMaximumValueError(ValidationError):
    def __init__(self, data: Any, maximum: Any) -> None:
        self.data = data
        self.maximum = maximum

        super().__init__("TODO...")


class InvalidMinimumLengthError(ValidationError):
    def __init__(self, data: Sized, minimum: Any) -> None:
        self.data = data
        self.minimum = minimum

        super().__init__("TODO...")


class InvalidMaximumLengthError(ValidationError):
    def __init__(self, data: Sized, maximum: Any) -> None:
        self.data = data
        self.maximum = maximum

        super().__init__("TODO...")


class InvalidPatternTypeError(ValidationError):
    def __init__(self, data: Union[str, bytes], regex: Pattern[Any]) -> None:
        self.data = data
        self.regex = regex

        super().__init__("TODO...")


class InvalidFormatError(ValidationError):
    def __init__(self, data: AnyStr, regex: Pattern[AnyStr]) -> None:
        self.data = data
        self.regex = regex

        super().__init__("TODO...")


class ItemValidationError(ValidationError):
    def __init__(self, error: TestplatesError) -> None:
        self.error = error

        super().__init__("TODO...")


class InvalidMinimumSizeError(ValidationError):
    def __init__(self, data: Sized, minimum: Any) -> None:
        self.data = data
        self.minimum = minimum

        super().__init__("TODO...")


class InvalidMaximumSizeError(ValidationError):
    def __init__(self, data: Sized, maximum: Any) -> None:
        self.data = data
        self.maximum = maximum

        super().__init__("TODO...")


class UniquenessError(ValidationError):
    def __init__(self, data: Sized) -> None:
        self.data = data

        super().__init__("TODO...")


class MemberValidationError(ValidationError):
    def __init__(self, enum_type: EnumMeta, member: Enum, error: Exception) -> None:
        self.enum_type = enum_type
        self.member = member
        self.error = error

        super().__init__("TODO...")


class FieldValidationError(ValidationError):
    def __init__(self, data: Any, key: str, error: TestplatesError) -> None:
        self.data = data
        self.key = key
        self.error = error

        super().__init__("TODO...")


class RequiredKeyMissingError(ValidationError):
    def __init__(self, data: Any, field: Any) -> None:
        self.data = data
        self.field = field

        super().__init__("TODO...")


class InvalidKeyError(ValidationError):
    def __init__(self, data: Any):
        self.data = data

        super().__init__("TODO...")


class ChoiceValidationError(ValidationError):
    def __init__(self, data: Any, error: TestplatesError):
        self.data = data
        self.error = error

        super().__init__("TODO...")
