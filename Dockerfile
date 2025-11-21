# Dockerfile for HooAah Yacht Chatbot
FROM python:3.11-slim

# Tesseract OCR 설치 (서버 환경)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-kor \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 포트 노출
EXPOSE 5000

# API 서버 실행
CMD ["python", "chatbot_unified.py", "--mode", "api", "--port", "5000"]

