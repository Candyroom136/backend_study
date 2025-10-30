#!/bin/bash

# 색상 코드
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     DB Trigger 테스트 (PostgreSQL + Tortoise ORM)     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Step 0: Python 버전 설정 (pyenv 사용)
echo -e "${BLUE}🔹 Step 0: Python 버전 설정${NC}"

# Python 3.12 사용 (asyncpg 호환)
REQUIRED_PYTHON="3.12"

if command -v pyenv &> /dev/null; then
    # pyenv로 Python 3.12 설치 여부 확인
    if pyenv versions | grep -q "$REQUIRED_PYTHON"; then
        echo "   ✓ Python $REQUIRED_PYTHON 설치됨"
    else
        echo "   Python $REQUIRED_PYTHON 설치 중..."
        pyenv install $REQUIRED_PYTHON
    fi

    # 로컬 Python 버전 설정
    pyenv local $REQUIRED_PYTHON
    echo "   ✓ Python $REQUIRED_PYTHON로 설정됨"
else
    echo -e "${YELLOW}   ⚠️  pyenv가 설치되지 않았습니다${NC}"
    echo "   현재 Python 버전을 사용합니다"
fi
echo ""

# Step 1: Docker 컨테이너 실행
echo -e "${BLUE}🔹 Step 1: Docker 컨테이너 확인${NC}"
if docker ps | grep -q trigger_test_db; then
    echo "   ✓ Docker 컨테이너 이미 실행 중"
else
    echo "   Docker 컨테이너 시작 중..."
    docker-compose -f docker-compose-trigger.yml up -d

    # PostgreSQL 준비 대기
    echo "   PostgreSQL 준비 대기 (5초)..."
    sleep 5

    if docker ps | grep -q trigger_test_db; then
        echo "   ✓ Docker 컨테이너 시작 완료"
    else
        echo -e "${RED}   ❌ Docker 컨테이너 시작 실패${NC}"
        exit 1
    fi
fi
echo ""

# Step 2: Python 버전 확인
echo -e "${BLUE}🔹 Step 2: Python 버전 확인${NC}"
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo "   현재 Python: $PYTHON_VERSION"
echo ""

# Step 3: 필요한 패키지 설치 확인
echo -e "${BLUE}🔹 Step 3: 필요한 패키지 확인${NC}"

# psycopg 확인
if python -c "import psycopg" 2>/dev/null; then
    echo "   ✓ psycopg 설치됨"
else
    echo "   psycopg 설치 중..."
    pip install psycopg
fi

# aerich & tortoise-orm & asyncpg 확인
if python -c "import aerich; import tortoise; import asyncpg" 2>/dev/null; then
    echo "   ✓ aerich, tortoise-orm, asyncpg 설치됨"
else
    echo "   aerich, tortoise-orm, asyncpg 설치 중..."
    pip install aerich tortoise-orm asyncpg
fi
echo ""

# Step 4: aerich 초기화
echo -e "${BLUE}🔹 Step 4: aerich 초기화${NC}"
if [ -f "pyproject.toml" ] && grep -q "tool.aerich" pyproject.toml 2>/dev/null; then
    echo "   ✓ aerich 이미 초기화됨"
else
    echo "   aerich 초기화 중..."
    aerich init -t tortoise_config.TORTOISE_ORM
    if [ $? -eq 0 ]; then
        echo "   ✓ aerich 초기화 완료"
    else
        echo -e "${RED}   ❌ aerich 초기화 실패${NC}"
        exit 1
    fi
fi
echo ""

# Step 5: 마이그레이션 적용 (aerich upgrade)
echo -e "${BLUE}🔹 Step 5: 마이그레이션 적용 (aerich upgrade)${NC}"
aerich upgrade
if [ $? -eq 0 ]; then
    echo "   ✓ 마이그레이션 적용 완료"
else
    echo -e "${RED}   ❌ 마이그레이션 적용 실패${NC}"
    exit 1
fi
echo ""

# Step 6: 테스트 실행
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "                    테스트 실행                            "
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python test_db_trigger.py

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "                    정리 명령어                            "
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Docker 중지: docker-compose -f docker-compose-trigger.yml down"
echo "DB 초기화: docker-compose -f docker-compose-trigger.yml down -v && rm -rf migrations/ pyproject.toml"
echo "DB 접속: psql -h localhost -p 5434 -U triggeruser -d triggerdb"
echo ""
