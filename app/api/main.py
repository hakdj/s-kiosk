from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
import sys
import os

# 🔧 sys.path 조작 없이 정식 경로 import
from app.core.database import get_db, init_db
from app.models.remote_command import RemoteCommand as CommandModel
from app.crud.remote_command import resend_command as crud_resend_command
from app.utils.utils import execute_query
from app.config.config import DB_NAME

app = FastAPI()

# ✅ 서버 시작할 때 DB 초기화
init_db()

# Pydantic Models (입력용)
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

class RemoteCommandCreate(BaseModel):
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
    return execute_query("SELECT * FROM payments", fetch=True)

@app.post("/status-log")
def add_status_log(log: StatusLog):
    execute_query(
        "INSERT INTO status_logs (kiosk_id, status, message, timestamp) VALUES (?, ?, ?, ?)",
        (log.kiosk_id, log.status, log.message, log.timestamp.isoformat())
    )
    return {"status": "status log saved"}

@app.get("/status-logs")
def list_status_logs():
    return execute_query("SELECT * FROM status_logs", fetch=True)

@app.post("/remote-command")
def add_remote_command(cmd: RemoteCommandCreate):
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
def add_multiple_remote_commands(cmds: List[RemoteCommandCreate]):
    for cmd in cmds:
        execute_query(
            "INSERT INTO remote_commands (kiosk_id, command, result, timestamp) VALUES (?, ?, ?, ?)",
            (cmd.kiosk_id, cmd.command, cmd.result, cmd.timestamp.isoformat())
        )
    return {"status": f"{len(cmds)} commands saved"}

@app.get("/remote-commands")
def list_all_remote_commands():
    return execute_query("SELECT * FROM remote_commands", fetch=True)

@app.post("/resend-command")
def resend_command_api(kiosk_id: str, db: Session = Depends(get_db)):
    result = crud_resend_command(db, kiosk_id)
    if not result:
        raise HTTPException(status_code=404, detail="명령어 없음")
    return {
        "message": "명령어 재전송 완료",
        "kiosk_id": result.kiosk_id,
        "received_at": result.received_at
    }
