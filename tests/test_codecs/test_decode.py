from typing import (
    Type,
    TypeVar,
)

from testplates import (
    struct,
    init,
    add_codec,
    Structure,
    decode,
    create_codec,
    TestplatesError,
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
    # noinspection PyUnusedLocal
    def decode_function(
        structure_type: Type[StructureTypeVar],
        data: bytes,
    ) -> Result[StructureTypeVar, TestplatesError]:
        return init(structure_type)

    codec = create_codec(unreachable, decode_function)

    @struct
    class Person:
        pass

    add_codec(Person, codec=codec)

    assert (decode_result := decode(Person, b""))
    assert isinstance(unwrap_success(decode_result), Person)


# noinspection PyTypeChecker
def test_decode_with_using() -> None:
    # noinspection PyUnusedLocal
    def decode_function(
        structure_type: Type[StructureTypeVar],
        data: bytes,
    ) -> Result[StructureTypeVar, TestplatesError]:
        return init(structure_type)

    primary = create_codec(unreachable, decode_function)
    secondary = create_codec(unreachable, unreachable)

    @struct
    class Person:
        pass

    add_codec(Person, codec=primary)
    add_codec(Person, codec=secondary)

    assert (decode_result := decode(Person, b"", using=primary))
    assert isinstance(unwrap_success(decode_result), Person)


# noinspection PyTypeChecker
def test_decode_failure() -> None:
    error = TestplatesError()

    # noinspection PyUnusedLocal
    def decode_function(
        structure_type: Type[StructureTypeVar],
        data: bytes,
    ) -> Result[StructureTypeVar, TestplatesError]:
        return failure(error)

    codec = create_codec(unreachable, decode_function)

    @struct
    class Person:
        pass

    add_codec(Person, codec=codec)

    assert not (encode_result := decode(Person, b""))
    assert unwrap_failure(encode_result) is error


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

    add_codec(Person, codec=first)

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

    add_codec(Person, codec=first)
    add_codec(Person, codec=second)

    assert not (encode_result := decode(Person, b""))

    error = unwrap_failure(encode_result)
    assert isinstance(error, AmbiguousCodecChoiceError)
    assert error.structure_type == Person
    assert error.codecs == [first, second]
