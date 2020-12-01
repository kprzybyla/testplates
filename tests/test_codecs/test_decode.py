from typing import (
    Type,
    TypeVar,
)

from testplates import (
    struct,
    init,
    field,
    attach_codec,
    Structure,
    decode,
    create_codec,
    TestplatesError,
    InvalidStructureError,
    NoCodecAvailableError,
    InaccessibleCodecError,
    AmbiguousCodecChoiceError,
)

from resultful import (
    failure,
    unwrap_success,
    unwrap_failure,
    Result,
)

from .utils import (
    unreachable,
)

StructureTypeVar = TypeVar("StructureTypeVar", bound=Structure)


# noinspection PyTypeChecker
def test_decode() -> None:
    metadata_object = object()

    # noinspection PyUnusedLocal
    def decode_function(
        metadata: object,
        structure_type: Type[StructureTypeVar],
        data: bytes,
    ) -> Result[StructureTypeVar, TestplatesError]:
        assert metadata is metadata_object
        return init(structure_type)

    codec = create_codec(unreachable, decode_function)

    @struct
    class Person:
        pass

    attach_codec(Person, codec=codec, metadata=metadata_object)

    assert (decode_result := decode(Person, b""))
    assert isinstance(unwrap_success(decode_result), Person)


# noinspection PyTypeChecker
def test_decode_without_metadata() -> None:
    # noinspection PyUnusedLocal
    def decode_function(
        metadata: None,
        structure_type: Type[StructureTypeVar],
        data: bytes,
    ) -> Result[StructureTypeVar, TestplatesError]:
        assert metadata is None
        return init(structure_type)

    codec = create_codec(unreachable, decode_function)

    @struct
    class Person:
        pass

    attach_codec(Person, codec=codec)

    assert (decode_result := decode(Person, b""))
    assert isinstance(unwrap_success(decode_result), Person)


# noinspection PyTypeChecker
def test_decode_with_using() -> None:
    # noinspection PyUnusedLocal
    def decode_function(
        metadata: None,
        structure_type: Type[StructureTypeVar],
        data: bytes,
    ) -> Result[StructureTypeVar, TestplatesError]:
        return init(structure_type)

    primary = create_codec(unreachable, decode_function)
    secondary = create_codec(unreachable, unreachable)

    @struct
    class Person:
        pass

    attach_codec(Person, codec=primary)
    attach_codec(Person, codec=secondary)

    assert (decode_result := decode(Person, b"", using=primary))
    assert isinstance(unwrap_success(decode_result), Person)


# noinspection PyTypeChecker
def test_decode_failure() -> None:
    error = TestplatesError()

    # noinspection PyUnusedLocal
    def decode_function(
        metadata: None,
        structure_type: Type[StructureTypeVar],
        data: bytes,
    ) -> Result[StructureTypeVar, TestplatesError]:
        return failure(error)

    codec = create_codec(unreachable, decode_function)

    @struct
    class Person:
        pass

    attach_codec(Person, codec=codec)

    assert not (encode_result := decode(Person, b""))
    assert unwrap_failure(encode_result) is error


# noinspection PyTypeChecker
def test_decode_failure_invalid_structure() -> None:
    field_error = TestplatesError()
    codec = create_codec(unreachable, unreachable)

    @struct
    class Person:
        name = field(failure(field_error))

    attach_codec(Person, codec=codec)

    assert not (encode_result := decode(Person, b""))

    error = unwrap_failure(encode_result)
    assert isinstance(error, InvalidStructureError)
    assert error.errors == [field_error]


# noinspection PyTypeChecker
def test_decode_failure_no_codec_available_error() -> None:
    @struct
    class Person:
        pass

    assert not (decode_result := decode(Person, b""))

    error = unwrap_failure(decode_result)
    assert isinstance(error, NoCodecAvailableError)
    assert error.structure_type == Person


# noinspection PyTypeChecker
def test_decode_failure_inaccessible_codec_error() -> None:
    first = create_codec(unreachable, unreachable)
    second = create_codec(unreachable, unreachable)

    @struct
    class Person:
        pass

    attach_codec(Person, codec=first)

    assert not (encode_result := decode(Person, b"", using=second))

    error = unwrap_failure(encode_result)
    assert isinstance(error, InaccessibleCodecError)
    assert error.structure_type == Person
    assert error.codecs == [first]
    assert error.using == second


# noinspection PyTypeChecker
def test_decode_failure_ambiguous_codec_choice_error() -> None:
    first = create_codec(unreachable, unreachable)
    second = create_codec(unreachable, unreachable)

    @struct
    class Person:
        pass

    attach_codec(Person, codec=first)
    attach_codec(Person, codec=second)

    assert not (encode_result := decode(Person, b""))

    error = unwrap_failure(encode_result)
    assert isinstance(error, AmbiguousCodecChoiceError)
    assert error.structure_type == Person
    assert error.codecs == [first, second]
