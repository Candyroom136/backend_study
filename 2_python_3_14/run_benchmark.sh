#!/bin/bash

# Python 버전별 벤치마크 자동 실행 스크립트

echo "=================================="
echo "Python 버전별 벤치마크 비교"
echo "=================================="
echo ""

# pyenv가 설치되어 있는지 확인
if ! command -v pyenv &> /dev/null; then
    echo "❌ pyenv가 설치되지 않았습니다."
    echo "   설치: brew install pyenv"
    exit 1
fi

# Python 3.13
echo "🔹 Python 3.13 실행 중..."
if pyenv versions --bare | grep -q "^3.13"; then
    pyenv local 3.13.5 2>/dev/null || pyenv local 3.13.0 2>/dev/null
    python benchmark.py
    echo ""
else
    echo "❌ Python 3.13이 설치되지 않았습니다."
    echo "   설치: pyenv install 3.13.0"
    echo ""
fi

echo ""

# Python 3.14
echo "🔹 Python 3.14 실행 중..."
if pyenv versions --bare | grep -q "^3.14.0$"; then
    pyenv local 3.14.0
    python benchmark.py
    echo ""
else
    echo "❌ Python 3.14가 설치되지 않았습니다."
    echo "   설치: pyenv install 3.14.0"
    echo ""
fi

echo ""

# Python 3.14t (Free-threaded)
echo "🔹 Python 3.14t (Free-threaded) 실행 중..."
if pyenv versions --bare | grep -q "3.14.0t"; then
    pyenv local 3.14.0t
    python benchmark.py
    echo ""
else
    echo "❌ Python 3.14t가 설치되지 않았습니다."
    echo "   설치: pyenv install 3.14.0t"
    echo ""
fi

# 원래 버전으로 복구
pyenv local --unset 2>/dev/null

echo "=================================="
echo "비교 완료!"
echo "=================================="
