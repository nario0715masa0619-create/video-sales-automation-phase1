import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("logs/send_log.db")

def init_send_log_db():
    """送信ログテーブルを初期化"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
    CREATE TABLE IF NOT EXISTS send_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        datetime TEXT NOT NULL,
        from_address TEXT NOT NULL,
        to_address TEXT NOT NULL,
        message_id TEXT UNIQUE NOT NULL,
        campaign_id TEXT,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    c.execute("""
    CREATE TABLE IF NOT EXISTS bounce_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT UNIQUE NOT NULL,
        sent_count INTEGER,
        bounce_count INTEGER,
        bounce_rate REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

def log_send_event(to_address, message_id, campaign_id="campaign_001", status="sent"):
    """送信ログを DB に記録"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
    INSERT INTO send_log (datetime, from_address, to_address, message_id, campaign_id, status)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        "marketing@luvira-biz.jp",
        to_address,
        message_id,
        campaign_id,
        status
    ))
    
    conn.commit()
    conn.close()

def get_todays_send_count():
    """本日の送信件数を集計"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    today = datetime.now().strftime("%Y-%m-%d")
    c.execute("""
    SELECT COUNT(*) FROM send_log
    WHERE date(datetime) = ? AND status = 'sent'
    """, (today,))
    
    count = c.fetchone()[0]
    conn.close()
    return count
