from typing import (
    Any,
    Union,
    Tuple,
    List,
    Iterable,
    Callable,
    Optional,
)

class MarkDecorator: ...

def param(
    *values: Any,
    marks: Union[MarkDecorator, Iterable[MarkDecorator]] = (),
    id: Optional[str] = None,
) -> Tuple[Any, Iterable[MarkDecorator], Optional[str]]: ...
def parametrize(
    argnames: str,
    argvalues: List[Any],
    indirect: bool = False,
    ids: Optional[List[str]] = None,
    scope: Optional[str] = None,
) -> Callable[..., Callable[..., None]]: ...
