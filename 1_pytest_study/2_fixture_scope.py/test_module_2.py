"""
Fixture Scope 테스트 - 간단 버전
"""

class TestClass:
    """테스트 클래스 - class scope 확인용"""
    
    def test_1(self, function_fixture, class_fixture, module_fixture, session_fixture):
        print(f"        테스트1: {function_fixture}")
        assert True
    
    def test_2(self, function_fixture, class_fixture, module_fixture, session_fixture):
        print(f"        테스트2: {function_fixture}")
        assert True

def test_standalone(function_fixture, class_fixture, module_fixture, session_fixture):
    """독립 함수 - 새로운 class scope 생성됨"""
    print(f"        독립테스트: {function_fixture}")
    assert True
