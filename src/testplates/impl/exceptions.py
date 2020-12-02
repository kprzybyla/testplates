__all__ = (
    "TestplatesError",
    "MissingValueError",
    "UnexpectedValueError",
    "ProhibitedValueError",
    "InvalidStructureError",
    "MissingBoundaryError",
    "InvalidSizeError",
    "UnlimitedRangeError",
    "MutuallyExclusiveBoundariesError",
    "OverlappingBoundariesError",
    "SingleMatchBoundariesError",
    "NoCodecAvailableError",
    "InaccessibleCodecError",
    "AmbiguousCodecChoiceError",
    "DefaultCodecAlreadySetError",
    "InvalidTypeValueError",
    "InvalidTypeError",
    "ProhibitedBoolValueError",
    "InvalidMinimumValueError",
    "InvalidMaximumValueError",
    "InvalidMinimumSizeError",
    "InvalidMaximumSizeError",
    "InvalidFormatError",
    "UniquenessError",
    "InvalidKeyError",
    "InvalidDataFormatError",
    "RequiredKeyMissingError",
    "UnknownFieldError",
    "MemberValidationError",
    "ItemValidationError",
    "FieldValidationError",
    "ChoiceValidationError",
)

from enum import (
    Enum,
    EnumMeta,
)

from typing import (
    Any,
    TypeVar,
    Tuple,
    Union,
    List,
    Sized,
    Pattern,
)

_GenericType = TypeVar("_GenericType")


class TestplatesError(Exception):

    """
    Base testplates error.
    """

    def __init__(
        self,
        *message: str,
    ):
        super().__init__(" ".join(message))

    @property
    def message(self) -> str:

        """
        Returns error message.
        """

        return "".join(self.args)


class MissingValueError(TestplatesError):

    """
    Error indicating missing value.

    Raised when user forgets to set mandatory
    value for given field with actual value.
    """

    def __init__(
        self,
        field: Any,
    ) -> None:
        self.field = field

        super().__init__(
            f"Missing value for required field {field!r}",
        )


class UnexpectedValueError(TestplatesError):

    """
    Error indicating unexpected value.

    Raised when user passes value which was
    not defined inside the template definition.
    """

    def __init__(
        self,
        key: str,
        value: Any,
    ) -> None:
        self.key = key
        self.value = value

        super().__init__(
            f"Unexpected key {key!r} with value {value!r}",
        )


class ProhibitedValueError(TestplatesError):

    """
    Error indicating prohibited value.

    Raised when user sets prohibited value that
    is invalid for given field due to its nature.
    """

    def __init__(
        self,
        field: Any,
        value: Any,
    ) -> None:
        self.field = field
        self.value = value

        super().__init__(
            f"Prohibited value {value!r} for field {field!r}",
        )


class InvalidStructureError(TestplatesError):

    """
    Error indicating invalid structure construction.

    Raised when user creates invalid structure,
    for example by passing validator which was
    not initialized properly to the field of
    this structure.
    """

    def __init__(self, errors: List[Any]) -> None:
        self.errors = errors

        super().__init__(
            f"Invalid structure construction due to following errors: {errors!r}",
        )


class MissingBoundaryError(TestplatesError):

    """
    Error indicating missing boundary.

    Raised when user forgets to set mandatory boundary
    for given template with minimum and maximum constraints.
    """

    def __init__(
        self,
        name: str,
    ) -> None:
        self.name = name

        super().__init__(
            f"Missing value for mandatory boundary {self.name!r}",
        )


class InvalidSizeError(TestplatesError):

    """
    Error indicating invalid size boundary value.

    Raised when user sets size boundary with value
    that does not meet size boundary requirements.
    """

    def __init__(
        self,
        boundary: Any,
    ) -> None:
        self.boundary = boundary

        super().__init__(
            f"Invalid value for size boundary {boundary!r}",
        )


class UnlimitedRangeError(TestplatesError):

    """
    Error indicating unlimited range.

    Raised when user sets both minimum and maximum
    boundaries to unlimited value in the context that
    does not allow such values to be used there together.
    """

    def __init__(self) -> None:
        super().__init__(
            "Unlimited range is not permitted in this context",
        )


class MutuallyExclusiveBoundariesError(TestplatesError):

    """
    Error indicating exclusive and inclusive boundaries collision.

    Raised when user sets mutually exclusive
    boundaries at the same time with value.
    """

    def __init__(
        self,
        name: str,
    ) -> None:
        self.name = name

        super().__init__(
            f"Mutually exclusive {name!r} boundaries set at the same time",
        )


class OverlappingBoundariesError(TestplatesError):

    """
    Error indicating overlapping boundaries.

    Raised when user sets both minimum and maximum
    boundaries with values the overlap over each other.
    """

    def __init__(
        self,
        minimum: Any,
        maximum: Any,
    ) -> None:
        self.minimum = minimum
        self.maximum = maximum

        super().__init__(
            f"Overlapping minimum {minimum!r} and maximum {maximum!r} boundaries",
        )


class SingleMatchBoundariesError(TestplatesError):

    """
    Error indicating single match boundaries range.

    Raised when user sets boundaries with values that
    creates range which matches only single value.
    """

    def __init__(
        self,
        minimum: Any,
        maximum: Any,
    ) -> None:
        self.minimum = minimum
        self.maximum = maximum

        super().__init__(
            f"Single match minimum {minimum!r} and maximum {maximum!r} boundaries",
        )


class NoCodecAvailableError(TestplatesError):

    """
    Error indicating no codec available for structure.

    Raised when user calls either encode or decode
    function for given structure which does not have
    any codec registered.
    """

    def __init__(
        self,
        structure_type: Any,
    ) -> None:
        self.structure_type = structure_type

        super().__init__(
            f"No codec available for structure type {structure_type!r}",
        )


class InaccessibleCodecError(TestplatesError):

    """
    Error indicating inaccessible codec for structure.

    Raised when user calls either encode or decode
    function for given structure and with specific
    codec set and given codec was not registered
    for that structure.
    """

    def __init__(
        self,
        structure_type: Any,
        codecs: List[Any],
        using: Any,
    ) -> None:
        self.structure_type = structure_type
        self.codecs = codecs
        self.using = using

        super().__init__(
            f"Codec {using!r} not available for structure type {structure_type!r}",
            f"(available: {codecs!r})",
        )


class AmbiguousCodecChoiceError(TestplatesError):

    """
    Error indicating ambiguous codec choice.

    Raised when user calls either encode or decode
    function for given structure that has multiple
    codecs registered but no default codec was
    registered and user didn't specify the codec
    which should be used.
    """

    def __init__(
        self,
        structure_type: Any,
        codecs: List[Any],
    ) -> None:
        self.structure_type = structure_type
        self.codecs = codecs

        super().__init__(
            f"Multiple codecs available for structure type {structure_type!r}",
            f"but no specific codec chosen (available: {codecs!r})",
        )


class DefaultCodecAlreadySetError(TestplatesError):

    """
    Error indicating that default codec was already set.

    Raised when user tries to set the default
    codec for the structure which already have
    default codec set.
    """

    def __init__(
        self,
        structure_type: Any,
        default_codec: Any,
        codec: Any,
    ) -> None:
        self.structure_type = structure_type
        self.default_codec = default_codec
        self.codec = codec

        super().__init__(
            f"Cannot set {codec!r} as default codec for {structure_type!r}",
            f"(already uses {default_codec!r})",
        )


class InvalidTypeValueError(TestplatesError):

    """
    Error indicating invalid type value.

    Raised when user passed value which is not a type
    or may not be used as the second argument of built-in
    isinstance() function (because it is not a classinfo).
    """

    def __init__(
        self,
        given_type: Any,
    ) -> None:
        self.given_type = given_type

        super().__init__(
            f"Given value {given_type!r} is not a type nor a classinfo",
        )


class InvalidTypeError(TestplatesError):

    """
    Error indicating invalid type.

    Raised when user passed a data which has a type
    not present in the specified allowed types tuple.
    """

    def __init__(
        self,
        data: Any,
        allowed_types: Tuple[type, ...],
    ) -> None:
        self.data = data
        self.allowed_types = allowed_types

        super().__init__(
            f"Invalid type {type(data)!r} of data {data!r} (allowed types: {allowed_types!r})",
        )


class ProhibitedBoolValueError(TestplatesError):

    """
    Error indicating prohibited bool value.

    Raised when user passed a data which has a bool type
    but the validator does not allow bool type values.
    """

    def __init__(
        self,
        data: bool,
    ) -> None:
        self.data = data

        super().__init__(
            f"Prohibited type {bool!r} of data {data!r}",
        )


class InvalidMinimumValueError(TestplatesError):

    """
    Error indicating invalid minimum value.

    Raised when user passed a data that does not match
    minimum value requirement specified by the validator.
    """

    def __init__(
        self,
        data: Any,
        minimum: Any,
    ) -> None:
        self.data = data
        self.minimum = minimum

        super().__init__(
            f"Invalid value {data!r} (minimum allowed value: {minimum!r})",
        )


class InvalidMaximumValueError(TestplatesError):

    """
    Error indicating invalid maximum value.

    Raised when user passed a data that does not match
    maximum value requirement specified by the validator.
    """

    def __init__(
        self,
        data: Any,
        maximum: Any,
    ) -> None:
        self.data = data
        self.maximum = maximum

        super().__init__(
            f"Invalid value {data!r} (maximum allowed value: {maximum!r})",
        )


class InvalidMinimumSizeError(TestplatesError):

    """
    Error indicating invalid minimum size.

    Raised when user passed a data that does not match
    minimum size requirement specified by the validator.
    """

    def __init__(
        self,
        data: Sized,
        minimum: Any,
    ) -> None:
        self.data = data
        self.minimum = minimum

        super().__init__(
            f"Invalid size {len(data)!r} of data {data!r} (minimum allowed size: {minimum!r})",
        )


class InvalidMaximumSizeError(TestplatesError):

    """
    Error indicating invalid maximum size.

    Raised when user passed a data that does not match
    maximum size requirement specified by the validator.
    """

    def __init__(
        self,
        data: Sized,
        maximum: Any,
    ) -> None:
        self.data = data
        self.maximum = maximum

        super().__init__(
            f"Invalid size {len(data)!r} of data {data!r} (maximum allowed size: {maximum!r})",
        )


class InvalidFormatError(TestplatesError):

    """
    Error indicating invalid data format.

    Raised when user passed a data that does not match
    the pattern requirement specified by the validator.
    """

    def __init__(
        self,
        data: Union[str, bytes],
        pattern: Pattern[Any],
    ) -> None:
        self.data = data
        self.pattern = pattern

        super().__init__(
            f"Invalid format of data {data!r} (allowed format: {pattern!r})",
        )


class UniquenessError(TestplatesError):

    """
    Error indicating not unique elements.

    Raised when user passed a data that contains
    not unique elements by the validator specified
    that all elements should be unique.
    """

    def __init__(
        self,
        data: Sized,
    ) -> None:
        self.data = data

        super().__init__(
            f"Data {data!r} does not contain unique elements",
        )


class InvalidKeyError(TestplatesError):

    """
    Error indicating invalid key.

    Raised when user passed a data that contains
    key that was not expected by the validator.
    """

    def __init__(
        self,
        key: str,
        data: Any,
    ) -> None:
        self.key = key
        self.data = data

        super().__init__(
            f"Invalid key {key!r} found in data {data!r}",
        )


class InvalidDataFormatError(TestplatesError):

    """
    Error indicating invalid data format.

    Raised when user passed a data which is a tuple
    but it contains more or less than two elements.
    """

    def __init__(
        self,
        data: Any,
    ) -> None:
        self.data = data

        super().__init__(
            f"Invalid data format found in data {data!r}",
        )


class RequiredKeyMissingError(TestplatesError):

    """
    Error indicating required key missing.


    Raised when user passed a data that is missing
    a mandatory key specified by the validator.
    """

    def __init__(
        self,
        data: Any,
        key: str,
        field: Any,
    ) -> None:
        self.data = data
        self.key = key
        self.field = field

        super().__init__(
            f"Mandatory key {key!r} ({field!r}) missing in data {data!r}",
        )


class UnknownFieldError(TestplatesError):

    """
    Error indicating unknown key for structure type.

    Raised when user passed a data that contains
    unknown key that was not specified by structure type.
    """

    def __init__(
        self,
        data: Any,
        structure_type: Any,
        key: str,
    ) -> None:
        self.data = data
        self.structure_type = structure_type
        self.key = key

        super().__init__(
            f"Unknown key {key!r} for structure type {structure_type!r} in {data!r}",
        )


class MemberValidationError(TestplatesError):

    """
    Error indicating member validation failure.

    Raised when member validation fails with
    any kind of error. This exception wraps
    the enum, member and error information.
    """

    def __init__(
        self,
        enum_type: EnumMeta,
        member: Enum,
        error: TestplatesError,
    ) -> None:
        self.enum_type = enum_type
        self.member = member
        self.error = error

        super().__init__(
            f"Member {member!r} validation failure in {enum_type!r}: {error!r}",
        )


class ItemValidationError(TestplatesError):

    """
    Error indicating item validation failure.

    Raised when item validation fails with
    any kind of error. This exception wraps
    the sequence, item and error information.
    """

    def __init__(
        self,
        data: Any,
        item: Any,
        error: TestplatesError,
    ) -> None:
        self.data = data
        self.item = item
        self.error = error

        super().__init__(
            f"Item {item!r} validation failure in {data!r}: {error!r}",
        )


class FieldValidationError(TestplatesError):

    """
    Error indicating field validation failure.

    Raised when field validation fails with
    any kind of error. This exception wraps
    the mapping, field and error information.
    """

    def __init__(
        self,
        data: Any,
        field: Any,
        error: TestplatesError,
    ) -> None:
        self.data = data
        self.field = field
        self.error = error

        super().__init__(
            f"Field {field!r} validation failure in {data!r}: {error!r}",
        )


class ChoiceValidationError(TestplatesError):

    """
    Error indicating choice validation failure.

    Raised when choice validation fails with
    any kind of error. This exception wraps
    the union, choice and error information.
    """

    def __init__(
        self,
        data: Any,
        validator: Any,
        error: TestplatesError,
    ) -> None:
        self.data = data
        self.validator = validator
        self.error = error

        super().__init__(
            f"Choice {validator!r} validation failure in {data!r}: {error!r}",
        )
