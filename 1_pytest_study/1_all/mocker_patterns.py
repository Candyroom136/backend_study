"""
Mocker 패턴 모음 - 다양한 사용법
"""
import requests
import json

# ===== 테스트할 함수들 =====
def get_weather(city):
    response = requests.get(f"https://api.weather.com/{city}")
    return response.json()

def save_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

class EmailService:
    def send(self, to, subject):
        # 실제 이메일 발송 로직
        return f"이메일 발송됨: {to}"

# ===== 패턴 1: 외부 API 모킹 =====
def test_weather_api(mocker):
    """외부 API 호출 모킹"""
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.json.return_value = {"temp": 25, "status": "sunny"}
    
    result = get_weather("서울")
    
    assert result["temp"] == 25
    mock_get.assert_called_once_with("https://api.weather.com/서울")

# ===== 패턴 2: 파일 시스템 모킹 =====
def test_save_file(mocker):
    """파일 저장 모킹"""
    mock_open = mocker.mock_open()
    mocker.patch('builtins.open', mock_open)
    
    save_to_file({"key": "value"}, "test.json")
    
    mock_open.assert_called_once_with("test.json", 'w')

# ===== 패턴 3: 클래스 메서드 모킹 =====
def test_email_service(mocker):
    """클래스 메서드 모킹"""
    mock_send = mocker.patch.object(EmailService, 'send')
    mock_send.return_value = "성공"
    
    service = EmailService()
    result = service.send("test@example.com", "제목")
    
    assert result == "성공"
    mock_send.assert_called_once_with("test@example.com", "제목")

# ===== 패턴 4: 여러 호출 결과 다르게 설정 =====
def test_multiple_calls(mocker):
    """여러 번 호출시 다른 결과"""
    mock_get = mocker.patch('requests.get')
    mock_get.side_effect = [
        mocker.Mock(json=lambda: {"result": "첫번째"}),
        mocker.Mock(json=lambda: {"result": "두번째"})
    ]
    
    result1 = get_weather("서울")
    result2 = get_weather("부산")
    
    assert result1["result"] == "첫번째"
    assert result2["result"] == "두번째"
    assert mock_get.call_count == 2

# ===== 패턴 5: 예외 발생 테스트 =====
def test_api_error(mocker):
    """API 에러 상황 테스트"""
    mock_get = mocker.patch('requests.get')
    mock_get.side_effect = requests.RequestException("네트워크 오류")
    
    import pytest
    with pytest.raises(requests.RequestException):
        get_weather("존재하지않는도시")

# ===== 패턴 6: 부분 모킹 (spy) =====
def test_spy_pattern(mocker):
    """실제 함수는 실행하되 호출만 감시"""
    spy = mocker.spy(json, 'dump')
    
    save_to_file({"test": "data"}, "real_file.json")
    
    # 실제로 json.dump가 호출되었는지 확인
    spy.assert_called_once()
