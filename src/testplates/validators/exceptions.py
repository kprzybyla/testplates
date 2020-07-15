from enum import Enum, EnumMeta
from typing import TypeVar

_T = TypeVar("_T")


class ValidationError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

        self.message = message


class InvalidTypeValueError(ValidationError):
    def __init__(self, given_type) -> None:
        self.given_type = given_type


class InvalidTypeError(ValidationError):
    def __init__(self, data, allowed_types) -> None:
        self.data = data
        self.allowed_types = allowed_types


class ProhibitedBooleanValueError(ValidationError):
    def __init__(self, data: bool) -> None:
        self.data = data


class InvalidMinimumValueError(ValidationError):
    def __init__(self, data, minimum) -> None:
        self.data = data
        self.minimum = minimum


class InvalidMaximumValueError(ValidationError):
    def __init__(self, data, maximum) -> None:
        self.data = data
        self.maximum = maximum


class InvalidLengthError(ValidationError):
    def __init__(self, data, length):
        self.data = data
        self.length = length


class InvalidMinimumLengthError(ValidationError):
    def __init__(self, data, minimum):
        self.data = data
        self.minimum = minimum


class InvalidMaximumLengthError(ValidationError):
    def __init__(self, data, maximum):
        self.data = data
        self.maximum = maximum


class InvalidPatternTypeError(ValidationError):
    def __init__(self, data, regex):
        self.data = data
        self.regex = regex


class InvalidFormatError(ValidationError):
    def __init__(self, data, regex):
        self.data = data
        self.regex = regex


class ItemValidationError(ValidationError):
    def __init__(self, error):
        self.error = error


class InvalidMinimumSizeError(ValidationError):
    def __init__(self, data, minimum):
        self.data = data
        self.minimum = minimum


class InvalidMaximumSizeError(ValidationError):
    def __init__(self, data, maximum):
        self.data = data
        self.maximum = maximum


class UniquenessError(ValidationError):
    def __init__(self, data):
        self.data = data


class MemberValidationError(ValidationError):
    def __init__(self, enum_type: EnumMeta, member: Enum, error: Exception) -> None:
        self.enum_type = enum_type
        self.member = member
        self.error = error


class FieldValidationError(ValidationError):
    def __init__(self, data, key, error):
        self.data = data
        self.key = key
        self.error = error


class RequiredKeyMissingError(ValidationError):
    def __init__(self, data, field) -> None:
        self.data = data
        self.field = field


class InvalidKeyError(ValidationError):
    def __init__(self, data):
        self.data = data


class ChoiceValidationError(ValidationError):
    def __init__(self, data, error):
        self.data = data
        self.error = error
