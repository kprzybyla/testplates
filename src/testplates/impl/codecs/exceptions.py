__all__ = (
    "NoCodecAvailableError",
    "InaccessibleCodecError",
    "AmbiguousCodecChoiceError",
    "DefaultCodecAlreadySetError",
)

from typing import (
    Any,
    List,
)

from testplates.impl.base import (
    TestplatesError,
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
