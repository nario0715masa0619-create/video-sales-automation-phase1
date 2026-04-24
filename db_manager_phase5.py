"""
db_manager_phase5.py
Web スクレイピング結果（Phase 5）を管理する DB モジュール
"""

import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("logs/phase5_data.db")

def init_phase5_db():
    """Phase 5 テーブルを初期化"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS phase5_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT NOT NULL,
        website_url TEXT UNIQUE NOT NULL,
        phone_number TEXT,
        email TEXT,
        status TEXT,
        scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    c.execute("""
    CREATE INDEX IF NOT EXISTS idx_website_url ON phase5_data(website_url)
    """)

    conn.commit()
    conn.close()

def check_url_exists(website_url):
    """URL が既に存在するか確認"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT id FROM phase5_data WHERE website_url = ?", (website_url,))
    result = c.fetchone()
    conn.close()

    return result is not None

def append_phase5_data(company_name, phone_number, email, status, website_url):
    """Phase 5 データを DB に保存"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    INSERT OR REPLACE INTO phase5_data
    (company_name, website_url, phone_number, email, status, updated_at)
    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (company_name, website_url, phone_number, email, status))

    conn.commit()
    conn.close()

def get_phase5_count():
    """Phase 5 データの総件数を取得"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM phase5_data")
    count = c.fetchone()[0]
    conn.close()

    return count
