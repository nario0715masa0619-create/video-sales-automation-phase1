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



def get_send_history(to_address):
    """メールアドレスの送信履歴を取得（通数と日付）"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
    SELECT COUNT(*), MAX(datetime) FROM send_log
    WHERE to_address = ? AND status = 'sent'
    """, (to_address,))
    
    result = c.fetchone()
    conn.close()
    
    if result[0] == 0:
        return 0, None  # 未送信
    return result[0], result[1]  # (送信済み通数, 最後の送信日時)

def get_next_email_num(to_address, interval_days=3):
    """次に送るべきメール通数を判定（3日ごとに次の通数へ）"""
    sent_count, last_sent_datetime = get_send_history(to_address)
    
    if sent_count == 0:
        return 1  # 未送信なら1通目
    
    if sent_count >= 4:
        return None  # 4通すべて送信済み
    
    if last_sent_datetime:
        last_sent = datetime.fromisoformat(last_sent_datetime)
        days_since = (datetime.now() - last_sent).days
        
        if days_since >= interval_days:
            return sent_count + 1  # 次の通数を返す
    
    return None  # まだタイミングではない
