import json
from pathlib import Path
import pytest

@pytest.fixture
def test_data():
    """JSON에서 테스트 데이터 로드"""
    data_file = Path(__file__).parent / "data" / "test_users.json"
    with open(data_file) as f:
        return json.load(f)

@pytest.mark.parametrize("user_data", [
    pytest.param(user, id=user["name"]) 
    for user in json.load(open("test_user.json"))
])
def test_user_validation(user_data):
    assert "email" in user_data
    assert "@" in user_data["email"]