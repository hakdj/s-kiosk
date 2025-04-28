# 🛠️ S-kiosk 프로젝트

![S-kiosk Banner](https://via.placeholder.com/1200x400?text=S-kiosk+Project)

---

## 📌 프로젝트 소개

**S-kiosk**는 키오스크 장비를 위한
**결제 처리, 원격 명령 전송, 상태 모니터링** 기능을 제공하는
**FastAPI + Streamlit** 기반 통합 관리자 시스템입니다.

---

## ✨ 주요 기능

- 💳 결제 이력 저장 및 조회
- 🔄 키오스크 원격 명령 전송 및 실행 결과 수신
- 📡 프린터, 네트워크 상태 모니터링
- 📈 관리자 대시보드에서 성공/실패 시각화
- 📁 CSV 다운로드 기능

---

## 🚀 실행 방법

### 1️⃣ Docker 설치

→ [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

### 2️⃣ 프로젝트 복제 및 실행

```bash
git clone https://github.com/hakdj/s-kiosk.git
cd s-kiosk
docker compose up --build
```

- 📂 **FastAPI Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- 📊 **Streamlit 관리자 대시보드**: [http://localhost:8501](http://localhost:8501)

---

## 📁 폴더 구조

```
s_kiosk_backend/
├── main.py                  # FastAPI API 서버
├── kiosk_dashboard.py       # Streamlit 대시보드
├── kiosk_agent.py           # 키오스크 명령 자동화
├── requirements.txt         # Python 패키지 목록
├── Dockerfile               # Docker 빌드 설정
├── docker-compose.yml       # Docker 통합 실행 설정
├── .gitignore               # Git 추적 제외 설정
└── README.md                # 프로젝트 설명 문서
```

---

## 🛠️ 기술 스택

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)

---

## 📜 라이선스

© 2025 SolidTech. All rights reserved.

---

## 🧠 추가 예정 항목 (Optional)

### 📷 데모 스크린샷

(향후 Streamlit 대시보드 및 Swagger UI 화면 캡처 추가 예정)

### 🗺️ 버전 히스토리

| 버전 | 날짜 | 설명 |
|------|------|------|
| v1.0 | 2025-04-24 | S-kiosk 프로젝트 최초 배포 |
