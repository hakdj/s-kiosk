from fastapi import APIRouter
from datetime import datetime
from app.utils.utils import execute_query  # 경로 맞는지 확인

router = APIRouter()

@router.get("/remote-commands")
def get_all_commands():
    rows = execute_query("SELECT * FROM remote_commands", fetch=True)

    formatted = []
    for row in rows:
        row = dict(row)

        for key in ['timestamp', 'received_at']:
            if row.get(key):
                try:
                    dt = datetime.fromisoformat(row[key])
                    row[key] = dt.strftime('%Y-%m-%d %H:%M:%S')  # ✅ 마이크로초 제거
                except Exception:
                    pass

        formatted.append(row)

    return formatted
