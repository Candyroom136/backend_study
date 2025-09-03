import pytest
import pytest_asyncio

@pytest_asyncio.fixture(params=["gpt-4o-mini", "gpt-4o", "gpt-4o-2024-08-06"])
async def llm_model(request):
    print(f"llm_model: {request.param}")
    return request.param

@pytest.mark.asyncio
async def test_chat(llm_model):
    # 이 테스트는 3번 실행됩니다 (각 llm마다 타입마다 실행)
    assert llm_model is not None
    assert "gpt" in llm_model