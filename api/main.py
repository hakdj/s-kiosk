from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from utils.utils import execute_query
from config.config import DB_NAME

app = FastAPI()

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

# API Routes
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
    return commands

@app.patch("/update-command")
def update_command_result(update: UpdateCommandResult):
    execute_query(
        "UPDATE remote_commands SET result = ? WHERE id = ?",
        (update.result, update.id)
    )
    return {"status": "updated"}

from utils.utils import init_db

# FastAPI 서버 시작 전에 DB 테이블 생성
init_db()
