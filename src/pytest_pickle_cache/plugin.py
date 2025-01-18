from __future__ import annotations

import base64
import binascii
import pickle
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any


@pytest.fixture(scope="session")
def use_cache(request: pytest.FixtureRequest) -> Callable[[str, Callable], Any]:
    """A pytest fixture to use cache.

    This fixture provides a caching mechanism for pytest, allowing you to
    store and retrieve objects using a specified key. The objects are serialized
    and deserialized using pickle and base64 encoding.
    """

    def use_cache(key: str, create: Callable[[], object]) -> Any:
        try:
            if value := request.config.cache.get(key, None):
                return pickle.loads(base64.b64decode(value))
        except (pickle.UnpicklingError, binascii.Error):
            request.config.cache.set(key, None)

        obj = create()
        value = base64.b64encode(pickle.dumps(obj)).decode("utf-8")

        request.config.cache.set(key, value)

        return obj

    return use_cache
