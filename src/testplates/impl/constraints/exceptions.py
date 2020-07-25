__all__ = ["InsufficientValuesError"]

from testplates.impl.base import TestplatesError


class InsufficientValuesError(TestplatesError):

    """
        Error indicating insufficient amount of values.

        Raised when user passes not enough values for template
        that accepts infinite number of values but requires at
        least a specific number of values to be provided.
    """

    def __init__(self, required: int) -> None:
        self.required = required

        super().__init__(f"Expected at least {required!r} value(s) to be provided")
