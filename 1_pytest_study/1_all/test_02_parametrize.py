
import pytest
from calculator import add


@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 5, 5)
])
@pytest.mark.asyncio
async def test_add_parametrized(a, b, expected):
    """parametrize 데코레이터 사용 예시"""
    result = await add(a, b)
    assert result == expected

@pytest.mark.parametrize("a", [
    2,3,4,
])
@pytest.mark.parametrize("b", [
    3,4,5,6
])
@pytest.mark.asyncio
async def test_multiple_add_parametrized(a, b):
    """parametrize 데코레이터 사용 예시"""
    result = await add(a, b)
    assert result == (a + b)