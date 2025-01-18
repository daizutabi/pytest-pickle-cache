"""Test the pytest_pickle_cache plugin."""

import datetime

import pytest
from pandas import DataFrame


def create() -> DataFrame:
    """Create a DataFrame with the current time."""
    now = datetime.datetime.now()
    return DataFrame({"now": [now]})


@pytest.fixture
def df(use_cache):
    return use_cache("use_cache", create)


def test_create(use_cache):
    df_cached = use_cache("use_cache", create)
    df_created = create()
    assert not df_created.equals(df_cached)
