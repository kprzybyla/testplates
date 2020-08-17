from typing import Any, TypeVar, Tuple, Union, Iterable, Callable, Optional, Literal

_Scope = Literal["session", "package", "module", "class", "function"]
_FixtureFunction = TypeVar("_FixtureFunction", bound=Callable[..., object])

class Config: ...

class FixtureFunctionMarker:
    scope: "Union[_Scope, Callable[[str, Config], _Scope]]"
    params: Optional[Tuple[object, ...]]
    autouse: bool
    ids: Union[Tuple[Union[None, str, float, int, bool], ...], Callable[[Any], Optional[object]]]
    name: Optional[str]
    def __call__(self, function: _FixtureFunction) -> _FixtureFunction: ...

def fixture(
    fixture_function: Optional[_FixtureFunction] = None,
    *args: Any,
    scope: "Union[_Scope, Callable[[str, Config], _Scope]]" = "function",
    params: Optional[Iterable[object]] = None,
    autouse: bool = False,
    ids: Optional[
        Union[Iterable[Union[None, str, float, int, bool]], Callable[[Any], Optional[object]]]
    ] = None,
    name: Optional[str] = None,
) -> Union[FixtureFunctionMarker, _FixtureFunction]: ...
