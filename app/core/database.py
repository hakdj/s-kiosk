from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./kiosk.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ✅ get_db 함수 추가 (FastAPI 의존성 주입용)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ 선택: 초기화용 (테이블 생성 등)
def init_db():
    from app.models.remote_command import RemoteCommand  # 지연 import로 순환참조 방지
    Base.metadata.create_all(bind=engine)
