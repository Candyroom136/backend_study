#!/bin/bash

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     t-string 실제 테스트 (PostgreSQL + psycopg3)          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# 1. Docker 확인 및 시작
echo "🔹 Step 1: PostgreSQL Docker 컨테이너 확인"
if ! docker ps | grep -q tstring_test_db; then
    echo "   Docker 컨테이너가 실행되지 않았습니다."
    echo "   시작 중..."
    docker-compose up -d
    echo "   PostgreSQL 준비 대기 (10초)..."
    sleep 10
else
    echo "   ✓ PostgreSQL 실행 중"
fi

echo ""

# 2. Python 버전 확인
echo "🔹 Step 2: Python 버전 확인"
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "   현재 Python: $PYTHON_VERSION"
else
    echo "   ❌ python3를 찾을 수 없습니다."
    exit 1
fi

# Python 3.14 사용 권장
if [[ $PYTHON_VERSION == 3.14* ]]; then
    echo "   ✓ Python 3.14 사용 중"
elif command -v pyenv &> /dev/null; then
    echo "   ⚠️  Python 3.14 권장, pyenv로 전환 시도"
    if pyenv versions --bare | grep -q "3.14.0t"; then
        pyenv local 3.14.0t
        PYTHON_CMD="python3"
        echo "   ✓ Python 3.14.0t로 전환"
    elif pyenv versions --bare | grep -q "^3.14.0$"; then
        pyenv local 3.14.0
        PYTHON_CMD="python3"
        echo "   ✓ Python 3.14.0으로 전환"
    else
        echo "   ⚠️  Python 3.14가 설치되지 않았습니다."
        echo "   설치: pyenv install 3.14.0t"
    fi
else
    echo "   ⚠️  Python 3.14 권장 (현재: $PYTHON_VERSION)"
fi

echo ""

# 3. psycopg3 확인
echo "🔹 Step 3: psycopg3 설치 확인"
if $PYTHON_CMD -c "import psycopg" 2>/dev/null; then
    echo "   ✓ psycopg3 설치됨"
else
    echo "   psycopg3가 설치되지 않았습니다."
    echo "   설치 중..."
    pip3 install "psycopg[binary]"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "                    테스트 실행                            "
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 4. 테스트 실행
$PYTHON_CMD test_tstring_real.py

EXIT_CODE=$?

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "                    정리 명령어                            "
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Docker 중지: docker-compose down"
echo "Docker 로그: docker-compose logs -f"
echo "DB 접속: psql -h localhost -p 5433 -U testuser -d testdb"
echo ""

exit $EXIT_CODE
