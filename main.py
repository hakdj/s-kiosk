from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import sqlite3

app = FastAPI(title="S-kiosk Backend API")

# SQLite DB 연결
conn = sqlite3.connect("kiosk.db", check_same_thread=False)
cursor = conn.cursor()

# 테이블 생성
cursor.execute('''
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kiosk_id TEXT,
    amount INTEGER,
    method TEXT,
    timestamp TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS status_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kiosk_id TEXT,
    status TEXT,
    detail TEXT,
    timestamp TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS commands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kiosk_id TEXT,
    command TEXT,
    result TEXT,
    timestamp TEXT
)
''')

conn.commit()

# 모델 정의
class Payment(BaseModel):
    kiosk_id: str
    amount: int
    method: str
    timestamp: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())

class StatusLog(BaseModel):
    kiosk_id: str
    status: str
    detail: str
    timestamp: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())

class RemoteCommand(BaseModel):
    kiosk_id: str
    command: str
    result: Optional[str] = "pending"
    timestamp: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())

class CommandUpdate(BaseModel):
    id: int
    result: str

# API 라우트
@app.post("/report-payment")
def report_payment(payment: Payment):
    cursor.execute("INSERT INTO payments (kiosk_id, amount, method, timestamp) VALUES (?, ?, ?, ?)",
                   (payment.kiosk_id, payment.amount, payment.method, payment.timestamp))
    conn.commit()
    return {"status": "success"}

@app.post("/report-status")
def report_status(status: StatusLog):
    cursor.execute("INSERT INTO status_logs (kiosk_id, status, detail, timestamp) VALUES (?, ?, ?, ?)",
                   (status.kiosk_id, status.status, status.detail, status.timestamp))
    conn.commit()
    return {"status": "logged"}

@app.post("/remote-command")
def send_command(command: RemoteCommand):
    cursor.execute("INSERT INTO commands (kiosk_id, command, result, timestamp) VALUES (?, ?, ?, ?)",
                   (command.kiosk_id, command.command, command.result, command.timestamp))
    conn.commit()
    return {"status": "command saved"}

@app.get("/payments")
def get_payments():
    cursor.execute("SELECT * FROM payments ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    return rows

@app.get("/status-logs")
def get_status_logs():
    cursor.execute("SELECT * FROM status_logs ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    return rows

@app.get("/commands")
def get_commands(
    kiosk_id: Optional[str] = Query(None),
    result: Optional[str] = Query(None)
):
    if kiosk_id and result:
        cursor.execute("SELECT * FROM commands WHERE kiosk_id = ? AND result = ? ORDER BY timestamp DESC", (kiosk_id, result))
    elif kiosk_id:
        cursor.execute("SELECT * FROM commands WHERE kiosk_id = ? ORDER BY timestamp DESC", (kiosk_id,))
    elif result:
        cursor.execute("SELECT * FROM commands WHERE result = ? ORDER BY timestamp DESC", (result,))
    else:
        cursor.execute("SELECT * FROM commands ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    return rows

@app.patch("/update-command")
def update_command(update: CommandUpdate):
    cursor.execute("UPDATE commands SET result = ? WHERE id = ?", (update.result, update.id))
    conn.commit()
    return {"status": "updated"}
