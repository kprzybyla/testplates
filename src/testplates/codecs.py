__all__ = (
    "encode",
    "decode",
    "get_codec",
    "create_codec",
    "set_default_codec",
    "Codec",
    "NoCodecAvailableError",
    "InaccessibleCodecError",
    "AmbiguousCodecChoiceError",
    "DefaultCodecAlreadySetError",
)

from typing import (
    Any,
    Type,
    TypeVar,
    Union,
    Optional,
)

from resultful import (
    success,
    failure,
    unwrap_success,
    Result,
)

from testplates.impl.base import (
    Structure,
)

from testplates.impl.base import (
    Codec as CodecImpl,
    EncodeFunction,
    DecodeFunction,
)

from .structure import (
    verify,
)

from .exceptions import (
    TestplatesError,
    NoCodecAvailableError,
    InaccessibleCodecError,
    AmbiguousCodecChoiceError,
    DefaultCodecAlreadySetError,
)

_Structure = TypeVar("_Structure", bound=Structure)
_GenericType = TypeVar("_GenericType")

Codec = Union[CodecImpl]


def encode(
    structure: Structure,
    /,
    *,
    using: Optional[Codec[Any]] = None,
    fallback: bool = False,
) -> Result[bytes, TestplatesError]:

    """
    Encodes structure into bytes using
    codec attached to that structure type.

    If there are multiple codecs attached to given structure type,
    `using` parameter value is used to define which codec should
    be chosen. If specified codec is not available and `fallback`
    is set to True, a default codec is going to be used if it was
    specified, otherwise, encode will return a failure.

    :failure NoCodecAvailableError:
        If no codec was registered for structure type.

    :failure InaccessibleCodecError:
        If specified codec is not available for structure type.

    :failure AmbiguousCodecChoiceError:
        If there are multiple codecs registered for structure type
        but no default codec available and no specific codec was demanded.

    :failure DefaultCodecAlreadySetError:
        If default codec is already available for structure
        type, and `override` is not set to `True`.

    :param structure: structure to be encoded
    :param using: defines which codec should be used for structure type
    :param fallback: allows fallback to the default codec from `using` codec
    """

    if not (verification_result := verify(structure)):
        return verification_result

    # TODO(kprzybyla): Implement template verification here
    # for value in structure._testplates_values_.values():
    #     if value is MISSING or value is ANY or value is WILDCARD:
    #         return failure(...)

    structure_type = type(structure)

    if not (codec_result := get_codec(structure_type, using=using, fallback=fallback)):
        return codec_result

    codec = unwrap_success(codec_result)
    metadata = codec.metadata.get(structure_type)

    if not (encode_result := codec.encode_function(metadata, structure)):
        return encode_result

    return encode_result


def decode(
    structure_type: Type[_Structure],
    data: bytes,
    *,
    using: Optional[Codec[Any]] = None,
    fallback: bool = False,
) -> Result[_Structure, TestplatesError]:

    """
    Decodes bytes into structure using
    codec attached to that structure type.

    If there are multiple codecs attached to given
    structure type, `using` parameter value is used
    to define which codec should be used.

    :failure NoCodecAvailableError:
        If no codec was registered for structure type.

    :failure InaccessibleCodecError:
        If specified codec is not available for structure type.

    :failure AmbiguousCodecChoiceError:
        If there are multiple codecs registered for structure type
        but no default codec available and no specific codec was demanded.

    :failure DefaultCodecAlreadySetError:
        If default codec is already available for structure
        type, and `override` is not set to `True`.

    :param structure_type: structure type to be decoded to
    :param data: bytes to be decoded
    :param using: defines which codec should be used for structure type
    :param fallback: allows fallback to the default codec from `using` codec
    """

    if not (verification_result := verify(structure_type)):
        return verification_result

    if not (codec_result := get_codec(structure_type, using=using, fallback=fallback)):
        return codec_result

    codec = unwrap_success(codec_result)
    metadata = codec.metadata.get(structure_type)

    if not (decode_result := codec.decode_function(metadata, structure_type, data)):
        return decode_result

    return decode_result


# noinspection PyProtectedMember
def get_codec(
    structure_type: Type[_Structure],
    /,
    *,
    using: Optional[Codec[Any]] = None,
    fallback: bool = False,
) -> Result[Codec[Any], TestplatesError]:

    """
    Retrieves codec from structure type.

    If there are multiple codecs attached to given
    structure type, `using` parameter value is used
    to define which codec should be used.

    :failure NoCodecAvailableError:
        If no codec was registered for structure type.

    :failure InaccessibleCodecError:
        If specified codec is not available for structure type.

    :failure AmbiguousCodecChoiceError:
        If there are multiple codecs registered for structure type
        but no default codec available and no specific codec was demanded.

    :param structure_type: structure type
    :param using: defines which codec should be used for structure type
    :param fallback: allows fallback to the default codec from `using` codec
    """

    codecs = structure_type._testplates_codecs_
    default_codec = structure_type._testplates_default_codec_

    if not codecs:
        return failure(NoCodecAvailableError(structure_type))

    if using is not None:
        try:
            index = codecs.index(using)
        except ValueError:
            if default_codec is not None and fallback:
                return success(default_codec)
            else:
                return failure(InaccessibleCodecError(structure_type, codecs, using))
        else:
            codec = codecs[index]
    else:
        if default_codec is not None:
            return success(default_codec)
        else:
            try:
                (codec,) = codecs
            except ValueError:
                return failure(AmbiguousCodecChoiceError(structure_type, codecs))

    return success(codec)


def create_codec(
    encode_function: EncodeFunction[_GenericType],
    decode_function: DecodeFunction[_GenericType],
) -> Codec[_GenericType]:

    """
    Creates codec with encode and decode functions.

    :param encode_function: codec encode function
    :param decode_function: codec decode function
    """

    return Codec(encode_function, decode_function)


# noinspection PyProtectedMember
def set_default_codec(
    structure_type: Type[_Structure],
    /,
    *,
    codec: Codec[Any],
    override: bool = False,
) -> Result[None, TestplatesError]:

    """
    Sets the default codec for structure type.

    :failure NoCodecAvailableError:
        If no codec was registered for structure type.

    :failure InaccessibleCodecError:
        If specified codec is not available structure type.

    :failure DefaultCodecAlreadySetError:
        If default codec is already available for structure
        type, and `override` is not set to `True`.

    :param structure_type: structure type
    :param codec: codec to be set as default codec
    :param override: allows override of the already existing default codec
    """

    codecs = structure_type._testplates_codecs_
    default_codec = structure_type._testplates_default_codec_

    if default_codec is not None and not override:
        return failure(DefaultCodecAlreadySetError(structure_type, default_codec, codec))

    if not codecs:
        return failure(NoCodecAvailableError(structure_type))

    if codec not in codecs:
        return failure(InaccessibleCodecError(structure_type, codecs, codec))

    structure_type._testplates_default_codec_ = codec

    return success(None)
