import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_get_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost") as client:
        response = await client.get("/users/1")
        assert response.status_code == 200
        assert response.json()["name"] == "김철수"

@pytest.mark.asyncio
async def test_get_nonexistent_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost") as client:
        response = await client.get("/users/999")
        assert response.status_code == 404
        assert "찾을 수 없습니다" in response.json()["detail"]

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost") as client:
        new_user = {"name": "박민수", "email": "park@example.com"}
        response = await client.post("/users", json=new_user)
        assert response.status_code == 200
        assert response.json()["name"] == "박민수"
        assert "id" in response.json()

@pytest.mark.asyncio
async def test_get_users():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost") as client:
        response = await client.get("/users")
        assert response.status_code == 200
        assert len(response.json()) == 3
        assert response.json()[0]["name"] == "김철수"
        assert response.json()[1]["name"] == "이영희"
        assert response.json()[2]["name"] == "박민수"


##coverage 알려줘야 함
## pytest --cov=main test_08_fastapi.py --cov-report=html
## /Users/jeongbinkim/Desktop/development/candyroom136/backend_study/1_pytest_study/live_coding/1_basic/htmlcov/index.html