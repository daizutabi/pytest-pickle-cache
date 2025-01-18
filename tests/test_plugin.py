import pytest


def test_fixture(pytester: pytest.Pytester):
    result = pytester.runpytest("--fixtures")
    assert "use_cache [session scope]" in result.stdout.str()


@pytest.fixture
def examples(pytester: pytest.Pytester):
    pytester.copy_example("tests/test_use_cache.py")


def test_use_cache(pytester: pytest.Pytester, examples):
    result = pytester.runpytest("-v")
    outcomes = result.parseoutcomes()
    assert outcomes["passed"] == 2
