import pytest
import time

@pytest.fixture
def slow_resource(request):
    """느린 리소스는 필요할 때만 생성"""
    if "slow" in request.keywords:
        print("느린 리소스 생성...")
        time.sleep(2)
        return "expensive_resource"
    return "mock_resource"

@pytest.mark.slow
def test_with_real_resource(slow_resource):
    assert slow_resource == "expensive_resource"

def test_with_mock_resource(slow_resource):
    assert slow_resource == "mock_resource"