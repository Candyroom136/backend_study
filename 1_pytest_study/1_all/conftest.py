import pytest 
import pytest_asyncio

@pytest_asyncio.fixture
def conftest_sample_numbers():
    return {"a": 10, "b": 5}