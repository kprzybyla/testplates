from enum import Enum, EnumMeta
from typing import TypeVar

_T = TypeVar("_T")


class ValidationError(Exception):
    pass


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
    pass


class InvalidMinimumLengthError(ValidationError):
    pass


class InvalidMaximumLengthError(ValidationError):
    pass


class InvalidPatternTypeError(ValidationError):
    pass


class InvalidFormatError(ValidationError):
    pass


class ItemValidationError(ValidationError):
    pass


class InvalidMinimumSizeError(ValidationError):
    pass


class InvalidMaximumSizeError(ValidationError):
    pass


class UniquenessError(ValidationError):
    pass


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


class ProhibitedValueError(ValidationError):
    pass


class RequiredKeyMissingError(ValidationError):
    def __init__(self, data, field) -> None:
        self.data = data
        self.field = field


class RequiredKeyValidatorMissingError(ValidationError):
    pass


class InvalidKeyError(ValidationError):
    pass


class ChoiceValidationError(ValidationError):
    def __init__(self, data, key, error):
        self.data = data
        self.key = key
        self.error = error


class EnumAliasesNotAllowed(ValidationError):
    pass
