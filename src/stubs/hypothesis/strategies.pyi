from typing import Optional

from .core import SearchStrategy

def integers(
    min_value: Optional[int] = None, max_value: Optional[int] = None
) -> SearchStrategy[int]: ...
