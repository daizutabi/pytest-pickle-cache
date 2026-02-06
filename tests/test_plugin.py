from __future__ import annotations

import pytest


def test_fixture(pytester: pytest.Pytester) -> None:
    result = pytester.runpytest("--fixtures")
    assert "use_cache [session scope]" in result.stdout.str()


@pytest.fixture
def examples(pytester: pytest.Pytester) -> None:
    pytester.copy_example("tests/test_use_cache.py")


def test_use_cache(pytester: pytest.Pytester, examples: None) -> None:
    assert examples is None
    result = pytester.runpytest("-v")
    outcomes = result.parseoutcomes()
    assert outcomes["passed"] == 2
