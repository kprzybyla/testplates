import pytest

import testplates

from .assets import ObjectStorage, MappingStorage


create_function_parameters = pytest.mark.parametrize(
    "create_function",
    [
        pytest.param(testplates.create_object, id="object"),
        pytest.param(testplates.create_mapping, id="mapping"),
    ],
)

create_function_and_storage_type_parameters = pytest.mark.parametrize(
    "create_function, storage_type",
    [
        pytest.param(testplates.create_object, ObjectStorage, id="object"),
        pytest.param(testplates.create_mapping, MappingStorage, id="mapping"),
    ],
)
