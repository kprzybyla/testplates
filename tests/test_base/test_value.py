from testplates.base.value import ANY, WILDCARD, ABSENT, MISSING


def test_repr_any() -> None:
    fmt = "testplates.ANY"

    assert repr(ANY) == fmt


def test_repr_wildcard() -> None:
    fmt = "testplates.WILDCARD"

    assert repr(WILDCARD) == fmt


def test_repr_absent() -> None:
    fmt = "testplates.ABSENT"

    assert repr(ABSENT) == fmt


def test_repr_missing() -> None:
    fmt = "testplates.MISSING"

    assert repr(MISSING) == fmt
