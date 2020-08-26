import pytest

from testplates import (
    create_object,
    create_mapping,
)

from .assets import (
    ObjectStorage,
    MappingStorage,
)


create_function_parameters = pytest.mark.parametrize(
    "create_function",
    [
        pytest.param(create_object, id="object"),
        pytest.param(create_mapping, id="mapping"),
    ],
)

create_function_and_storage_type_parameters = pytest.mark.parametrize(
    "create_function, storage_type",
    [
        pytest.param(create_object, ObjectStorage, id="object"),
        pytest.param(create_mapping, MappingStorage, id="mapping"),
    ],
)
