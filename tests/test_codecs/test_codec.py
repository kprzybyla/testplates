from testplates import (
    struct,
    attach_codec,
    get_codec,
    create_codec,
    set_default_codec,
    NoCodecAvailableError,
    InaccessibleCodecError,
    DefaultCodecAlreadySetError,
)

from resultful import (
    unwrap_success,
    unwrap_failure,
)

from .utils import (
    unreachable,
)


# noinspection PyTypeChecker
def test_add_codec() -> None:
    codec = create_codec(unreachable, unreachable)

    @struct
    class Person:
        pass

    attach_codec(Person, codec=codec)

    assert (result := get_codec(Person))
    assert unwrap_success(result) is codec


# noinspection PyTypeChecker
def test_default_codec() -> None:
    main = create_codec(unreachable, unreachable)
    default = create_codec(unreachable, unreachable)

    @struct
    class Person:
        pass

    attach_codec(Person, codec=main)
    attach_codec(Person, codec=default)

    assert set_default_codec(Person, codec=default)
    assert (result := get_codec(Person))

    codec = unwrap_success(result)
    assert codec is default


# noinspection PyTypeChecker
def test_default_codec_with_fallback() -> None:
    main = create_codec(unreachable, unreachable)
    other = create_codec(unreachable, unreachable)
    default = create_codec(unreachable, unreachable)

    @struct
    class Person:
        pass

    attach_codec(Person, codec=main)
    attach_codec(Person, codec=default)

    assert set_default_codec(Person, codec=default)
    assert (result := get_codec(Person, using=other, fallback=True))

    codec = unwrap_success(result)
    assert codec is default


# noinspection PyTypeChecker
def test_default_codec_override() -> None:
    primary = create_codec(unreachable, unreachable)
    secondary = create_codec(unreachable, unreachable)

    @struct
    class Person:
        pass

    attach_codec(Person, codec=primary)
    attach_codec(Person, codec=secondary)

    assert set_default_codec(Person, codec=primary)
    assert set_default_codec(Person, codec=secondary, override=True)
    assert (result := get_codec(Person))

    codec = unwrap_success(result)
    assert codec is secondary


# noinspection PyTypeChecker
def test_default_codec_failure_default_codec_already_set_error() -> None:
    primary = create_codec(unreachable, unreachable)
    secondary = create_codec(unreachable, unreachable)

    @struct
    class Person:
        pass

    attach_codec(Person, codec=primary)
    attach_codec(Person, codec=secondary)

    assert set_default_codec(Person, codec=primary)
    assert not (result := set_default_codec(Person, codec=secondary))

    error = unwrap_failure(result)
    assert isinstance(error, DefaultCodecAlreadySetError)
    assert error.structure_type == Person
    assert error.default_codec == primary
    assert error.codec == secondary


# noinspection PyTypeChecker
def test_default_codec_failure_no_codec_available_error() -> None:
    codec = create_codec(unreachable, unreachable)

    @struct
    class Person:
        pass

    assert not (result := set_default_codec(Person, codec=codec))

    error = unwrap_failure(result)
    assert isinstance(error, NoCodecAvailableError)
    assert error.structure_type == Person


# noinspection PyTypeChecker
def test_default_codec_failure_inaccessible_codec_error() -> None:
    primary = create_codec(unreachable, unreachable)
    secondary = create_codec(unreachable, unreachable)

    @struct
    class Person:
        pass

    attach_codec(Person, codec=primary)

    assert not (result := set_default_codec(Person, codec=secondary))

    error = unwrap_failure(result)
    assert isinstance(error, InaccessibleCodecError)
    assert error.structure_type == Person
    assert error.codecs == [primary]
    assert error.using == secondary


# noinspection PyTypeChecker
def test_default_codec_without_fallback_failure_inaccessible_codec_error() -> None:
    main = create_codec(unreachable, unreachable)
    other = create_codec(unreachable, unreachable)
    default = create_codec(unreachable, unreachable)

    @struct
    class Person:
        pass

    attach_codec(Person, codec=main)
    attach_codec(Person, codec=default)

    assert set_default_codec(Person, codec=default)
    assert not (result := get_codec(Person, using=other))

    error = unwrap_failure(result)
    assert isinstance(error, InaccessibleCodecError)
    assert error.structure_type == Person
    assert error.codecs == [main, default]
    assert error.using == other
