import pytest
from calculator import add, divide

@pytest.mark.asyncio
async def test_add():
    assert await add(2, 3) == 5
    assert await add(-1, 1) == 0
    # TIP: 부동소수점 비교 시 pytest.approx 사용
    assert await add(0.1, 0.2) == pytest.approx(0.3)

@pytest.mark.asyncio
async def test_divide():
    assert await divide(10, 2) == 5
    
@pytest.mark.asyncio
async def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        await divide(10, 0)

