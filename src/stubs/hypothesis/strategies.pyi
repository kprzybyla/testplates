from typing import Any, AnyStr, TypeVar, Tuple, Union, List, Callable, Hashable, Pattern, Optional

from .core import SearchStrategy

Ex = TypeVar("Ex", covariant=True)

UniqueBy = Union[Callable[[Ex], Hashable], Tuple[Callable[[Ex], Hashable], ...]]

def integers(
    min_value: Optional[int] = None, max_value: Optional[int] = None
) -> SearchStrategy[int]: ...
def lists(
    elements: SearchStrategy[Ex],
    min_size: int = 0,
    max_size: Optional[int] = None,
    unique_by: Optional[UniqueBy[Ex]] = None,
    unique: bool = False,
) -> SearchStrategy[List[Ex]]: ...
def from_regex(
    regex: Union[AnyStr, Pattern[AnyStr]], fullmatch: bool = False
) -> SearchStrategy[AnyStr]: ...
def data() -> SearchStrategy[DataObject]: ...

class DataObject:
    def draw(self, strategy: SearchStrategy[Ex], label: Any = None) -> Ex: ...
