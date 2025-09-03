import pytest
import pytest_asyncio
from tortoise import Tortoise
from testcontainers.postgres import PostgresContainer
from models import User

@pytest_asyncio.fixture(scope="session")
async def db_container():
    """세션 시작시 PostgreSQL 컨테이너만 시작"""
    _container = PostgresContainer("postgres:13")
    _container.with_exposed_ports(5432)
    _container.start()
    print(f'\n=== PostgreSQL 컨테이너 시작 ===')
    print(f'호스트 포트: {_container.get_exposed_port(5432)}')

    yield _container

    """세션 종료시 컨테이너 정리"""
    if _container:
        print('\n=== PostgreSQL 컨테이너 중지 ===')
        _container.stop()

@pytest.fixture(scope="session")
def db_url(db_container):
    """데이터베이스 URL 제공"""
    url = db_container.get_connection_url()
    return url.replace("postgresql+psycopg2://", "postgres://")

@pytest_asyncio.fixture
async def db_setup(db_url):
    """각 테스트마다 새로운 TortoiseORM 연결"""
    # 조용히 DB 연결 및 스키마 생성
    await Tortoise.init(
        db_url=db_url,
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()
    
    # 테스트 실행 전 데이터 정리
    await User.all().delete()
    
    yield
    
    # 테스트 후 정리 및 연결 종료  
    await User.all().delete()
    await Tortoise.close_connections()

