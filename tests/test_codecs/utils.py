from typing import (
    Any,
    NoReturn,
)


# noinspection PyUnusedLocal
def unreachable(*args: Any, **kwargs: Any) -> NoReturn:
    assert False
