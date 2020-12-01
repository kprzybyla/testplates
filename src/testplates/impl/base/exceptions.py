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
)

from typing import (
    Any,
    List,
)


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
