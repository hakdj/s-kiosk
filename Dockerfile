# 베이스 이미지 (Python 3.10 기반, 용량 작음)
FROM python:3.10-slim

# 컨테이너 안에서 작업할 디렉토리
WORKDIR /app

# 모든 파일 복사
COPY . /app

# pip 업그레이드 및 의존성 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 실행 명령은 docker-compose에서 처리
