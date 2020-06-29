from testplates import UNLIMITED


def test_repr_unlimited() -> None:
    fmt = "testplates.UNLIMITED"

    assert repr(UNLIMITED) == fmt
