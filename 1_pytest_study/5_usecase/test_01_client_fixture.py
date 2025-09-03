import pytest
from fastapi.testclient import TestClient
from jose import jwt
from main import app

@pytest.fixture
def client():
    """테스트 클라이언트"""
    return TestClient(app)

@pytest.fixture
def authenticated_client(client):
    """인증된 클라이언트"""
    import time
    # JWT 토큰 생성 (1시간 후 만료)
    token_data = {"sub": "testuser", "exp": int(time.time()) + 3600}
    token = jwt.encode(token_data, "secret_key", algorithm="HS256")
    
    client.headers = {"Authorization": f"Bearer {token}"}
    return client

def test_protected_endpoint(authenticated_client):
    response = authenticated_client.get("/protected/profile")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"