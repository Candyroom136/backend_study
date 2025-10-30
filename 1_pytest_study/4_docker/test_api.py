import pytest
import requests

def test_health_check(docker_services):
    """헬스체크 API 테스트"""
    response = requests.get("http://localhost:8000/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "user-service"
    assert data["database"] == "connected"

def test_get_all_users(docker_services):
    """전체 사용자 조회 API 테스트 (실제 DB)"""
    response = requests.get("http://localhost:8000/users")
    assert response.status_code == 200
    
    data = response.json()
    assert "users" in data
    assert len(data["users"]) == 3
    assert data["users"][0]["name"] == "김철수"

def test_get_user_by_id(docker_services):
    """특정 사용자 조회 API 테스트"""
    response = requests.get("http://ec2-3-38-105-120.ap-northeast-2.compute.amazonaws.com:8000/users/1")   
    assert response.status_code == 200
    
    data = response.json()
    assert data["user"]["id"] == 1
    assert data["user"]["name"] == "김철수"
    assert data["user"]["email"] == "kim@example.com"

def test_get_nonexistent_user(docker_services):
    """존재하지 않는 사용자 조회 테스트"""
    response = requests.get("http://localhost:8000/users/999")
    assert response.status_code == 404
    
    data = response.json()
    assert data["detail"] == "User not found"

def test_create_user(docker_services):
    """사용자 생성 API 테스트 (실제 DB)"""
    new_user = {
        "name": "최신규",
        "email": "choi@example.com"
    }
    
    response = requests.post("http://localhost:8000/users", json=new_user)
    if response.status_code != 200:
        print(f"❌ 요청 실패: {response.status_code}")
        print(f"❌ 응답: {response.text}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["user"]["name"] == "최신규"
    assert data["user"]["email"] == "choi@example.com"
    assert "id" in data["user"]  # 자동 생성된 ID
    assert data["message"] == "User created"
    
    # 생성된 사용자 조회 확인
    user_id = data["user"]["id"]
    response = requests.get(f"http://localhost:8000/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["user"]["name"] == "최신규"

def test_database_integration(docker_services):
    """데이터베이스 통합 테스트"""
    # 현재 사용자 수 확인
    response = requests.get("http://localhost:8000/users")
    initial_count = len(response.json()["users"])
    
    # 새 사용자 생성
    new_user = {"name": "통합테스트", "email": "integration@test.com"}
    response = requests.post("http://localhost:8000/users", json=new_user)
    assert response.status_code == 200
    
    # 사용자 수 증가 확인
    response = requests.get("http://localhost:8000/users")
    new_count = len(response.json()["users"])
    assert new_count == initial_count + 1
    
    # 마지막 사용자가 방금 생성한 사용자인지 확인
    users = response.json()["users"]
    last_user = users[-1]
    assert last_user["name"] == "통합테스트"
    assert last_user["email"] == "integration@test.com"

@pytest.mark.slow
def test_api_performance(docker_services):
    """API 성능 테스트 (slow 마크)"""
    import time
    
    start = time.time()
    for _ in range(10):
        response = requests.get("http://localhost:8000/users")
        assert response.status_code == 200
    
    elapsed = time.time() - start
    assert elapsed < 5.0  # 10번 호출이 5초 이내에 완료되어야 함