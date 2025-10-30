# Python 3.14 테스트

Python 3.13 vs 3.14/3.14t 성능 및 기능 비교

## 📁 파일 구조

```
2_python_3_14/
├── benchmark.py              # Free-threading 성능 벤치마크
├── run_benchmark.sh          # 벤치마크 실행 스크립트
├── test_tstring.py           # t-string vs f-string 테스트
├── run_test_tstring.sh       # t-string 테스트 실행 스크립트
└── README.md
```

## 🚀 실행 방법

### 1. Free-threading 벤치마크 (Python 3.13, 3.14, 3.14t 비교)

```bash
chmod +x run_benchmark.sh
./run_benchmark.sh
```

**테스트 내용:**
- GIL 있을 때 vs 없을 때 멀티스레드 성능 비교
- CPU 집약적 작업 (factorial 계산)
- 예상 결과: 3.14t에서 약 4배 성능 향상

### 2. t-string 테스트 (Python 3.14+)

```bash
chmod +x run_test_tstring.sh
./run_test_tstring.sh
```

**테스트 내용:**
1. SQL Injection 방어 비교
2. XSS 공격 방어 비교
3. f-string vs t-string 성능 비교

## 📋 필요한 것

### pyenv 설치
```bash
# Mac
brew install pyenv

# shell 설정 (zsh)
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc
```

### Python 버전 설치
```bash
# Python 3.13
pyenv install 3.13.0

# Python 3.14
pyenv install 3.14.0

# Python 3.14t (Free-threaded) - 추천
pyenv install 3.14.0t

# 설치 확인
pyenv versions
```

## 📊 예상 결과

### Free-threading 벤치마크
```
Python 3.13:   1.09x (GIL로 병렬화 효과 없음)
Python 3.14:   1.10x (여전히 GIL)
Python 3.14t:  3.91x (GIL 제거, 4배 빠름!)
```

### t-string 테스트
```
SQL Injection:  f-string 취약 → t-string 안전
XSS 공격:       f-string 취약 → t-string 안전
성능:           t-string이 약간 느림 (보안 trade-off)
```

## 💡 핵심 정리

### Free-threading (GIL 제거)
- ✅ CPU bound 작업에서 4배 성능 향상
- ❌ 싱글 스레드는 약간 느려짐 (trade-off)
- 📌 멀티 스레드 필요한 경우에만 사용

### t-string
- ✅ SQL/XSS 자동 방어
- ✅ 라이브러리가 안전하게 처리
- ❌ 약간의 성능 저하
- 📌 보안이 중요한 경우 사용

## 🔧 문제 해결

### pyenv 명령어가 안 될 때
```bash
# shell 설정 확인
cat ~/.zshrc | grep pyenv

# 없으면 다시 설정
eval "$(pyenv init -)"
```

### Python 버전 전환
```bash
# 특정 버전으로 전환
pyenv local 3.14.0t

# 확인
python --version

# 원래대로
pyenv local --unset
```
