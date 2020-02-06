from typing import Any, TypeVar, Generic, Union, Callable

T = TypeVar("T")

Ex = TypeVar("Ex", covariant=True)

def given(
    *_given_arguments: Union[SearchStrategy[T], InferType],
    **_given_kwargs: Union[SearchStrategy[T], InferType],
) -> Callable[[Callable[..., None]], Callable[..., None]]: ...
def assume(condition: Any) -> bool: ...

class SearchStrategy(Generic[Ex]): ...
class InferType: ...
