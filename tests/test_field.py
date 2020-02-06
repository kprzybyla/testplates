import pytest

from typing import Any

from testplates import field, Required, DanglingDescriptorError


def test_name_raises_dangling_descriptor_error_when_specified_outside_the_class() -> None:
    key: Required[Any] = field()

    with pytest.raises(DanglingDescriptorError):
        print(key.name)
