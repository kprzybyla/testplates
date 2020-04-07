__all__ = ["Constraint"]

import abc

from .template import Template


class Constraint(Template, abc.ABC):

    __slots__ = ()
