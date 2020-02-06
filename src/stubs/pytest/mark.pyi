from typing import Any, List, Callable, Optional

def parametrize(
    argnames: str,
    argvalues: List[Any],
    indirect: bool = False,
    ids: Optional[List[str]] = None,
    scope: Optional[str] = None,
) -> Callable[..., Callable[..., None]]: ...
