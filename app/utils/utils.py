import sqlite3
import os
from app.config.config import DB_NAME


# ✅ 프로젝트 루트로 고정
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", DB_NAME)
DB_PATH = os.path.abspath(DB_PATH)

def execute_query(query: str, params: tuple = (), fetch: bool = False):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return result

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

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
            message TEXT,
            timestamp TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS remote_commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kiosk_id TEXT,
            command TEXT,
            result TEXT,
            timestamp TEXT,
            received_at TEXT
        )
    ''')

    conn.commit()
    conn.close()