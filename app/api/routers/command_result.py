from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import sqlite3

router = APIRouter()
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../../s_kiosk.db"))


# 📌 kiosk_id 기반 명령 결과 보고 모델
class CommandResultReport(BaseModel):
    kiosk_id: str
    result: str
    received_at: datetime

# ✅ kiosk_id 기준으로 가장 최근 명령어의 결과를 업데이트
@router.post("/command-result")
def report_command_result_by_kiosk(data: CommandResultReport):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE remote_commands
            SET result = ?, received_at = ?
            WHERE id = (
                SELECT id FROM remote_commands
                WHERE kiosk_id = ?
                ORDER BY timestamp DESC
                LIMIT 1
            )
        """, (data.result, data.received_at.isoformat(), data.kiosk_id))

        conn.commit()
        conn.close()

        return {"message": "✅ kiosk_id 기반 명령 결과 업데이트 완료"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
