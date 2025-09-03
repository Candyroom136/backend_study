import requests

# ===== 테스트할 함수들 =====
def get_user_info(user_id):
    """외부 API에서 사용자 정보 가져오기"""
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()

class EmailService:
    def __init__(self, api_key):
        self.api_key = api_key
    
    def send_email(self, to, subject, body):
        """이메일 발송"""
        # 실제로는 외부 이메일 서비스 호출
        return f"이메일 발송: {to} - {subject}"

# ===== 패턴 1: 기본 API 모킹 =====
def test_basic_api_mocking(mocker):
    """기본 API 호출 모킹"""
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.json.return_value = {"id": 1, "name": "김철수", "email": "kim@test.com"}
    
    result = get_user_info(1)
    
    assert result["name"] == "김철수"
    assert result["email"] == "kim@test.com"


# ===== 패턴 2: 클래스 메서드 모킹 =====
def test_class_method_mocking(mocker):
    """클래스 메서드 모킹"""
    mock_send = mocker.patch.object(EmailService, 'send_email')
    mock_send.return_value = "이메일 발송 성공"
    
    service = EmailService("fake_api_key")
    result = service.send_email("test@example.com", "안녕하세요", "테스트 메시지")
    
    assert result == "이메일 발송 성공"

# ===== 패턴 3: 선택적 모킹 (결제 API만 모킹) =====
def test_selective_mocking(mocker):
    """특정 URL만 모킹, 나머지는 실제 호출"""
    def selective_mock(url, *args, **kwargs):
        if "payment" in url:
            # 결제 API만 모킹
            mock_response = mocker.Mock()
            mock_response.json.return_value = {"status": "success", "transaction_id": "12345"}
            return mock_response
        else:
            # 나머지는 실제 호출
            return mocker.patch.object(requests, 'get').return_value
    
    mock_get = mocker.patch('requests.get', side_effect=selective_mock)
    
    # 결제 API 호출 (모킹됨)
    payment_response = requests.get("https://api.payment.com/charge")
    payment_result = payment_response.json()
    
    assert payment_result["status"] == "success"
    assert payment_result["transaction_id"] == "12345"
