from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import List
from utils.utils import execute_query, init_db
from config.config import DB_NAME
from fastapi import Depends
from sqlalchemy.orm import Session
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from models import RemoteCommand


app = FastAPI()

# ✅ 서버 시작할 때 DB 초기화
init_db()

# Models
class Payment(BaseModel):
    kiosk_id: str
    amount: int
    method: str
    timestamp: datetime

class StatusLog(BaseModel):
    kiosk_id: str
    status: str
    message: str
    timestamp: datetime

class RemoteCommand(BaseModel):
    kiosk_id: str
    command: str
    result: Optional[str] = "pending"
    timestamp: datetime

class UpdateCommandResult(BaseModel):
    id: int
    result: str

# API
@app.post("/payment")
def add_payment(payment: Payment):
    execute_query(
        "INSERT INTO payments (kiosk_id, amount, method, timestamp) VALUES (?, ?, ?, ?)",
        (payment.kiosk_id, payment.amount, payment.method, payment.timestamp.isoformat())
    )
    return {"status": "payment saved"}

@app.get("/payments")
def list_payments():
    payments = execute_query("SELECT * FROM payments", fetch=True)
    return payments

@app.post("/status-log")
def add_status_log(log: StatusLog):
    execute_query(
        "INSERT INTO status_logs (kiosk_id, status, message, timestamp) VALUES (?, ?, ?, ?)",
        (log.kiosk_id, log.status, log.message, log.timestamp.isoformat())
    )
    return {"status": "status log saved"}

@app.get("/status-logs")
def list_status_logs():
    logs = execute_query("SELECT * FROM status_logs", fetch=True)
    return logs

@app.post("/remote-command")
def add_remote_command(cmd: RemoteCommand):
    execute_query(
        "INSERT INTO remote_commands (kiosk_id, command, result, timestamp) VALUES (?, ?, ?, ?)",
        (cmd.kiosk_id, cmd.command, cmd.result, cmd.timestamp.isoformat())
    )
    return {"status": "command saved"}

@app.get("/commands")
def get_pending_commands(kiosk_id: str, result: str = "pending"):
    commands = execute_query(
        "SELECT * FROM remote_commands WHERE kiosk_id = ? AND result = ?",
        (kiosk_id, result),
        fetch=True
    )
    
    # 명령어를 내려줄 때 received_at을 지금 시간으로 업데이트
    for cmd in commands:
        execute_query(
            "UPDATE remote_commands SET received_at = ? WHERE id = ?",
            (datetime.now().isoformat(), cmd["id"])
        )
    
    return commands

@app.patch("/update-command")
def update_command_result(update: UpdateCommandResult):
    execute_query(
        "UPDATE remote_commands SET result = ? WHERE id = ?",
        (update.result, update.id)
    )
    return {"status": "updated"}

@app.post("/remote-command-bulk")
def add_multiple_remote_commands(cmds: List[RemoteCommand]):
    for cmd in cmds:
        execute_query(
            "INSERT INTO remote_commands (kiosk_id, command, result, timestamp) VALUES (?, ?, ?, ?)",
            (cmd.kiosk_id, cmd.command, cmd.result, cmd.timestamp.isoformat())
        )
    return {"status": f"{len(cmds)} commands saved"}


@app.get("/remote-commands")
def list_all_remote_commands():
    commands = execute_query(
        "SELECT * FROM remote_commands",
        fetch=True
    )
    return commands

@app.post("/resend-command")
async def resend_command(kiosk_id: str, db: Session = Depends(get_db)):
    # 1. 재전송할 명령어 찾기
    command = db.query(RemoteCommand).filter(
        RemoteCommand.kiosk_id == kiosk_id,
        RemoteCommand.status == "pending"  # (상황에 따라 수정 가능)
    ).first()

    if not command:
        return {"error": "명령어 없음"}

    # 2. 명령어를 실제 키오스크로 보내는 로직 (여기는 네 기존 로직에 맞게 수정)
    # send_to_kiosk(kiosk_id, command.command_data)

    # 3. 전송 성공했으면 received_at 업데이트
    command.received_at = datetime.utcnow().isoformat()
    db.commit()

    return {"message": "명령어 재전송 완료", "kiosk_id": kiosk_id}
