"""Test the pytest_pickle_cache plugin."""

from __future__ import annotations

import datetime
import time
from typing import TYPE_CHECKING

import pytest
from pandas import DataFrame

if TYPE_CHECKING:
    from pytest_pickle_cache import UseCache


def create() -> DataFrame:
    now = datetime.datetime.now()  # noqa: DTZ005
    return DataFrame({"now": [now]})


@pytest.fixture
def df(use_cache: UseCache[DataFrame]) -> DataFrame:
    return use_cache("use_cache", create)


def test_create(use_cache: UseCache[DataFrame]) -> None:
    df_cached = use_cache("use_cache", create)
    time.sleep(1)
    df_created = create()
    assert not df_created.equals(df_cached)


def test_create_df(df: DataFrame, use_cache: UseCache[DataFrame]) -> None:
    df_cached = use_cache("use_cache", create)
    assert df.equals(df_cached)
