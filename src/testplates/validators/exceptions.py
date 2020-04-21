class ValidatorError(Exception):
    pass


class InvalidTypeError(ValidatorError):
    pass


class InvalidMinimumValueError(ValidatorError):
    pass


class InvalidMaximumValueError(ValidatorError):
    pass


class InvalidLengthError(ValidatorError):
    pass


class InvalidMinimumLengthError(ValidatorError):
    pass


class InvalidMaximumLengthError(ValidatorError):
    pass


class InvalidPatternTypeError(ValidatorError):
    pass


class InvalidFormatError(ValidatorError):
    pass
