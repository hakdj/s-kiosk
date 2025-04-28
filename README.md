# 🛠️ S-kiosk 프로젝트

`S-kiosk`는 키오스크 장비를 위한 **결제 처리, 상태 모니터링, 원격 명령 실행** 기능을 포함한  
**FastAPI + Streamlit 기반 통합 관리 시스템**입니다.

---

## 🚀 실행 방법 (Docker 기반)



s_kiosk_backend/
├── main.py                  # FastAPI 백엔드 API
├── kiosk_dashboard.py       # Streamlit 대시보드 UI
├── kiosk_agent.py           # 키오스크 명령 처리 자동화 코드
├── requirements.txt         # 필요한 Python 라이브러리 목록
├── Dockerfile               # Docker 빌드 설정
├── docker-compose.yml       # 통합 실행 설정
├── .gitignore               # Git 추적 제외 파일 설정
└── README.md                # 현재 문서





```bash
docker compose up --build


📂 FastAPI Swagger UI: http://localhost:8000/docs

📊 Streamlit 관리자 대시보드: http://localhost:8501

처음만 --build 사용, 그 다음부터는 docker compose up만 사용해도 됩니다.