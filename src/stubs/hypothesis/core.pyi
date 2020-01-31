from typing import Any, TypeVar, Generic, Union, Callable

T = TypeVar("T")

class SearchStrategy(Generic[T]): ...
class InferType: ...

def given(
    *_given_arguments: Union[SearchStrategy[T], InferType],
    **_given_kwargs: Union[SearchStrategy[T], InferType],
) -> Callable[[Callable[..., None]], Callable[..., None]]: ...
def assume(condition: Any) -> bool: ...
