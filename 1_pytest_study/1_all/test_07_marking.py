import pytest 

@pytest.mark.unit
@pytest.mark.asyncio
async def test_unit():
    assert True

@pytest.mark.integration
@pytest.mark.asyncio
async def test_integration():
    assert True

@pytest.mark.e2e
@pytest.mark.asyncio
async def test_e2e():
    assert True

## pytest -m "e2e"
## pytest -m "not e2e"