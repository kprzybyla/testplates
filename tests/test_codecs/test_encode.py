from testplates import (
    struct,
    init,
    field,
    attach_codec,
    Structure,
    encode,
    create_codec,
    TestplatesError,
    InvalidStructureError,
    NoCodecAvailableError,
    InaccessibleCodecError,
    AmbiguousCodecChoiceError,
)

from resultful import (
    success,
    failure,
    unwrap_success,
    unwrap_failure,
    Result,
)

from hypothesis import (
    given,
    strategies as st,
)

from .utils import (
    unreachable,
)


# noinspection PyTypeChecker
@given(data=st.binary())
def test_encode(data: bytes) -> None:
    metadata_object = object()

    # noinspection PyUnusedLocal
    def encode_function(
        metadata: object,
        structure: Structure,
    ) -> Result[bytes, TestplatesError]:
        assert metadata is metadata_object
        return success(data)

    codec = create_codec(encode_function, unreachable)

    @struct
    class Person:
        pass

    attach_codec(Person, codec=codec, metadata=metadata_object)

    assert (person_result := init(Person))

    person = unwrap_success(person_result)
    assert (encode_result := encode(person))
    assert unwrap_success(encode_result) == data


# noinspection PyTypeChecker
@given(data=st.binary())
def test_encode_without_metadata(data: bytes) -> None:
    # noinspection PyUnusedLocal
    def encode_function(
        metadata: None,
        structure: Structure,
    ) -> Result[bytes, TestplatesError]:
        assert metadata is None
        return success(data)

    codec = create_codec(encode_function, unreachable)

    @struct
    class Person:
        pass

    attach_codec(Person, codec=codec)

    assert (person_result := init(Person))

    person = unwrap_success(person_result)
    assert (encode_result := encode(person))
    assert unwrap_success(encode_result) == data


# noinspection PyTypeChecker
@given(data=st.binary())
def test_encode_with_using(data: bytes) -> None:
    # noinspection PyUnusedLocal
    def encode_function(
        metadata: None,
        structure: Structure,
    ) -> Result[bytes, TestplatesError]:
        return success(data)

    primary = create_codec(encode_function, unreachable)
    secondary = create_codec(unreachable, unreachable)

    @struct
    class Person:
        pass

    attach_codec(Person, codec=primary)
    attach_codec(Person, codec=secondary)

    assert (person_result := init(Person))

    person = unwrap_success(person_result)
    assert (encode_result := encode(person, using=primary))
    assert unwrap_success(encode_result) is data


# noinspection PyTypeChecker
def test_encode_failure() -> None:
    error = TestplatesError()

    # noinspection PyUnusedLocal
    def encode_function(
        metadata: None,
        structure: Structure,
    ) -> Result[bytes, TestplatesError]:
        return failure(error)

    codec = create_codec(encode_function, unreachable)

    @struct
    class Person:
        pass

    attach_codec(Person, codec=codec)

    assert (person_result := init(Person))

    person = unwrap_success(person_result)
    assert not (encode_result := encode(person))
    assert unwrap_failure(encode_result) is error


# noinspection PyTypeChecker
@given(name=st.text())
def test_encode_failure_invalid_structure(name: str) -> None:
    field_error = TestplatesError()
    codec = create_codec(unreachable, unreachable)

    @struct
    class Person:
        name = field(failure(field_error))

    attach_codec(Person, codec=codec)

    person = Person(name=name)
    assert not (encode_result := encode(person))

    error = unwrap_failure(encode_result)
    assert isinstance(error, InvalidStructureError)
    assert error.errors == [field_error]


# noinspection PyTypeChecker
def test_encode_failure_no_codec_available_error() -> None:
    @struct
    class Person:
        pass

    assert (person_result := init(Person))

    person = unwrap_success(person_result)
    assert not (encode_result := encode(person))

    error = unwrap_failure(encode_result)
    assert isinstance(error, NoCodecAvailableError)
    assert error.structure_type == Person


# noinspection PyTypeChecker
def test_encode_failure_inaccessible_codec_error() -> None:
    first = create_codec(unreachable, unreachable)
    second = create_codec(unreachable, unreachable)

    @struct
    class Person:
        pass

    attach_codec(Person, codec=first)

    assert (person_result := init(Person))

    person = unwrap_success(person_result)
    assert not (encode_result := encode(person, using=second))

    error = unwrap_failure(encode_result)
    assert isinstance(error, InaccessibleCodecError)
    assert error.structure_type == Person
    assert error.codecs == [first]
    assert error.using == second


# noinspection PyTypeChecker
def test_encode_failure_ambiguous_codec_choice_error() -> None:
    primary = create_codec(unreachable, unreachable)
    secondary = create_codec(unreachable, unreachable)

    @struct
    class Person:
        pass

    attach_codec(Person, codec=primary)
    attach_codec(Person, codec=secondary)

    assert (person_result := init(Person))

    person = unwrap_success(person_result)
    assert not (encode_result := encode(person))

    error = unwrap_failure(encode_result)
    assert isinstance(error, AmbiguousCodecChoiceError)
    assert error.structure_type == Person
    assert error.codecs == [primary, secondary]
