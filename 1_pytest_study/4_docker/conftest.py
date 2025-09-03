# conftest.py
import pytest
import docker
import time
import requests
import subprocess
from testcontainers.postgres import PostgresContainer
import os

# 전역 컨테이너 관리
_postgres_container = None

@pytest.fixture(scope="session")
def postgres_container():
    """PostgreSQL 테스트 컨테이너 시작"""
    global _postgres_container
    print('\n=== PostgreSQL 테스트 컨테이너 시작 ===')
    _postgres_container = PostgresContainer("postgres:13")
    _postgres_container.with_exposed_ports(5432)
    _postgres_container.start()
    
    # 포트 정보 출력
    db_port = _postgres_container.get_exposed_port(5432)
    db_url = _postgres_container.get_connection_url()
    print(f'PostgreSQL 포트: {db_port}')
    print(f'DB URL: {db_url}')
    
    yield _postgres_container
    
    print('\n=== PostgreSQL 테스트 컨테이너 중지 ===')
    _postgres_container.stop()

@pytest.fixture(scope="session")
def docker_services(postgres_container):
    """Docker Compose 환경 시작/종료 (host.docker.internal 사용)"""
    # PostgreSQL URL을 환경변수로 설정 (host.docker.internal 사용)
    db_port = postgres_container.get_exposed_port(5432)
    postgres_url = f"postgresql://test:test@host.docker.internal:{db_port}/test"
    
    # 환경변수 설정
    env = os.environ.copy()
    env.update({
        'DATABASE_URL': postgres_url,
        'POSTGRES_HOST': 'host.docker.internal',
        'POSTGRES_PORT': str(db_port),
        'POSTGRES_DB': postgres_container.dbname,
        'POSTGRES_USER': postgres_container.username,
        'POSTGRES_PASSWORD': postgres_container.password,
        'ENV': 'test'
    })
    
    print(f'\n=== Docker 이미지 빌드 (최신 코드 반영) ===')
    subprocess.run(
        ["docker", "build", "-t", "user-service-test", "."],
        check=True
    )
    
    print(f'\n=== Docker Compose 시작 (host.docker.internal 사용) ===')
    print(f'DATABASE_URL: {postgres_url}')
    
    # Docker Compose 시작 (환경변수 전달)
    subprocess.run(
        ["docker-compose", "-f", "docker-compose.test.yml", "up", "-d"],
        env=env,
        check=True
    )
    
    # 서비스가 준비될 때까지 대기
    wait_for_services()
    
    yield
    
    # 정리
    print('\n=== Docker Compose 중지 ===')
    subprocess.run(["docker-compose", "-f", "docker-compose.test.yml", "down"])

def wait_for_services(max_wait=60):
    """서비스들이 준비될 때까지 대기"""
    services = [
        ("http://localhost:8000/health", "User Service")
    ]
    
    for url, name in services:
        print(f'{name} 대기 중...')
        start_time = time.time()
        
        while True:
            elapsed = time.time() - start_time
            if elapsed > max_wait:
                print(f"❌ {name}가 {max_wait}초 내에 준비되지 않았습니다")
                pytest.fail(f"{name}가 {max_wait}초 내에 준비되지 않았습니다")
                
            try:
                print(f"  - {name} 연결 시도 중... ({elapsed:.1f}초 경과)")
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    print(f"✅ {name} 준비 완료!")
                    break
                else:
                    print(f"  - 응답 코드: {response.status_code}")
            except requests.exceptions.ConnectionError as e:
                print(f"  - 연결 실패: {e}")
            except requests.exceptions.Timeout as e:
                print(f"  - 타임아웃: {e}")
            except Exception as e:
                print(f"  - 기타 오류: {e}")
                
            time.sleep(2)  # 2초 간격으로 재시도