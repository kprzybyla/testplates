import pytest

import testplates

from .assets import ObjectStorage, MappingStorage


template_parameters = pytest.mark.parametrize(
    "template_type",
    [
        pytest.param(testplates.Object, id="object"),
        pytest.param(testplates.Mapping, id="mapping"),
    ],
)

template_and_storage_parameters = pytest.mark.parametrize(
    "template_type, storage_type",
    [
        pytest.param(testplates.Object, ObjectStorage, id="object"),
        pytest.param(testplates.Mapping, MappingStorage, id="mapping"),
    ],
)
