import pytest
import pytest_asyncio
from calculator import add, divide

@pytest_asyncio.fixture
async def sample_numbers():
    """테스트에서 사용할 샘플 숫자들"""
    return {"a": 10, "b": 5}

@pytest.mark.asyncio
async def test_add_with_fixture(sample_numbers):
    result = await add(sample_numbers["a"], sample_numbers["b"])
    assert result == 15

@pytest.mark.asyncio
async def test_divide_with_fixture(conftest_sample_numbers):
    result = await divide(conftest_sample_numbers["a"], conftest_sample_numbers["b"])
    assert result == 2.0