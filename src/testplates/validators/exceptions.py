class ValidationError(Exception):
    pass


class InvalidTypeError(ValidationError):
    def __init__(self, data, allowed_types):
        self.data = data
        self.allowed_types = allowed_types


class ProhibitedBooleanValueError(ValidationError):
    pass


class InvalidMinimumValueError(ValidationError):
    pass


class InvalidMaximumValueError(ValidationError):
    pass


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
    pass


class FieldValidationError(ValidationError):
    pass


class ProhibitedValueError(ValidationError):
    pass


class RequiredKeyMissingError(ValidationError):
    pass


class RequiredKeyValidatorMissingError(ValidationError):
    pass


class InvalidKeyError(ValidationError):
    pass


class ChoiceValidationError(ValidationError):
    pass


class EnumAliasesNotAllowed(ValidationError):
    pass
