__all__ = ["Object", "Mapping"]

from typing import Any

from .object import Object as _Object
from .mapping import Mapping as _Mapping

Object = _Object[Any]
Mapping = _Mapping[Any]
