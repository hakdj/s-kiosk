import sqlite3
import os
from config.config import DB_NAME

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, DB_NAME)

# ✅ 여기에 테이블 생성 함수 추가
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
            timestamp TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
