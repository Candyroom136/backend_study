import pytest_asyncio

@pytest_asyncio.fixture(scope="function")  # 기본값: 각 테스트마다 새로 생성
def function_fixture():
    print("\n      함수시작")
    yield 'function_fixture'
    print("\n      함수종료")

@pytest_asyncio.fixture(scope="class")  # 클래스당 한 번만 생성
def class_fixture():
    print("\n    클래스시작")
    yield 'class_fixture'
    print("\n    클래스종료")

@pytest_asyncio.fixture(scope="module")  # 모듈당 한 번만 생성
async def module_fixture():
    print("\n  모듈시작")
    yield 'module_fixture'
    print("\n  모듈종료")

@pytest_asyncio.fixture(scope="session", autouse=True)  # 전체 테스트 세션당 한 번만 생성
async def session_fixture():
    print("\n세션시작")
    yield 'session_fixture'
    print("\n세션종료")