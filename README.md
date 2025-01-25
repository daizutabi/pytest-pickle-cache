# pytest-pickle-cache

[![PyPI Version][pypi-v-image]][pypi-v-link]
[![Python Version][python-v-image]][python-v-link]
[![Build Status][GHAction-image]][GHAction-link]
[![Coverage Status][codecov-image]][codecov-link]

## Overview

`pytest-pickle-cache` is a pytest plugin for caching test results using pickle.
By utilizing this plugin, you can reduce test execution time and perform tests
more efficiently.

## Installation

You can install `pytest-pickle-cache` using the following command:

```bash
pip install pytest-pickle-cache
```

## Fixture

The `use_cache` fixture is a pytest fixture that provides a caching mechanism
for pytest, allowing you to store and retrieve objects using a specified key.
The objects are serialized and deserialized using pickle and base64 encoding.

```python
def use_cache(key: str, func: Callable[[], Any]) -> Any:
    """Retrieve a cached result or execute the function if not cached.

    Args:
        key (str): The key to identify the cached result.
        func (Callable[[], Any]): The function to execute if the result is
            not cached. The result of the function is serialized and stored
            in the cache for future use.

    Returns:
        Any: The cached result or the result of the executed function.
    """
```

## Example

Here is a specific example of how to use `pytest-pickle-cache` to cache test results.

```python
import datetime

import pytest
from pandas import DataFrame


def create() -> DataFrame:
    """Create a DataFrame with the current time."""
    now = datetime.datetime.now()
    return DataFrame({"now": [now]})


def test_create(use_cache):
    """Create a DataFrame using cache and compare the results."""
    # Retrieve DataFrame using cache
    df_cached = use_cache("key", create)

    # Create a new DataFrame
    df_created = create()

    # Assert that the cached DataFrame and the newly created DataFrame are different.
    assert not df_created.equals(df_cached)


def test_create_with_cache(use_cache):
    """Use cache to retrieve the same DataFrame and ensure the results are the same."""
    # Cache the DataFrame on the first call
    df_cached_first = use_cache("key", create)

    # Call the same function again to retrieve from cache
    df_cached_second = use_cache("key", create)

    # Assert that the cached DataFrame is the same on the second call.
    assert df_cached_first.equals(df_cached_second)
```


You can also use `use_cache` fixture as a fixture in your test file.

```python
@pytest.fixture
def df(use_cache):
    return use_cache("key", create)
```

You can also use `use_cache` fixture with a parametrized fixture.

```python
def create(param: int) -> DataFrame:
    """Create a DataFrame with the current time."""
    now = datetime.datetime.now()
    return DataFrame({"now": [now], "param": [param]})


@pytest.fixture(params=[1, 2, 3])
def df(use_cache, request):
    return use_cache(f"key_{request.param}", lambda: create(request.param))
```

## Benefits

- **Efficiency in Testing**: By using `pytest-pickle-cache`, you can avoid running
the same test multiple times, reducing the overall test execution time.

- **Consistency of Results**: Using cache ensures that you get the same result
for the same input, maintaining consistency in your tests.

<!-- Badges -->
[pypi-v-image]: https://img.shields.io/pypi/v/pytest-pickle-cache.svg
[pypi-v-link]: https://pypi.org/project/pytest-pickle-cache/
[python-v-image]: https://img.shields.io/pypi/pyversions/pytest-pickle-cache.svg
[python-v-link]: https://pypi.org/project/pytest-pickle-cache
[GHAction-image]: https://github.com/daizutabi/pytest-pickle-cache/actions/workflows/ci.yml/badge.svg?branch=main&event=push
[GHAction-link]: https://github.com/daizutabi/pytest-pickle-cache/actions?query=event%3Apush+branch%3Amain
[codecov-image]: https://codecov.io/github/daizutabi/pytest-pickle-cache/coverage.svg?branch=main
[codecov-link]: https://codecov.io/github/daizutabi/pytest-pickle-cache?branch=main
