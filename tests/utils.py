import random

from typing import (
    TypeVar,
    List,
    Iterable,
)

_T = TypeVar("_T")


def sample(data: Iterable[_T], /) -> _T:
    return random.choice(list(data))


def samples(values: List[_T], /, *, minimum: int = 0) -> List[_T]:
    return random.sample(values, k=random.randint(minimum, len(values)))
