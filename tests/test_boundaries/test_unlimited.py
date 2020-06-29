from testplates import UNLIMITED


def test_repr() -> None:
    fmt = "testplates.UNLIMITED"

    assert repr(UNLIMITED) == fmt
