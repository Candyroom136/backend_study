import json
from pathlib import Path
import pytest

@pytest.fixture
def test_data():
    """JSON에서 테스트 데이터 로드"""
    data_file = Path(__file__).parent / "test_user.json"
    with open(data_file) as f:
        return json.load(f)

def test_user_validation(test_data):
    """fixture를 사용한 테스트"""
    for user in test_data:
        assert "email" in user
        assert "@" in user["email"]

# parametrize를 사용한 개별 테스트
@pytest.mark.parametrize("user_data", [
    pytest.param(user, id=user["name"]) 
    for user in json.load(open(Path(__file__).parent / "test_user.json"))
])
def test_individual_user_validation(user_data):
    """각 사용자별 개별 테스트"""
    assert "email" in user_data
    assert "@" in user_data["email"]