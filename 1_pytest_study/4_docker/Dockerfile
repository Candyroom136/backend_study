FROM python:3.11-slim

WORKDIR /app

# curl 설치 (헬스체크용)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# 필요한 패키지 설치
COPY requirements.txt .
RUN pip install -r requirements.txt

# 앱 복사
COPY . .

# 포트 노출
EXPOSE 8000

# 앱 실행
CMD ["python", "main.py"]