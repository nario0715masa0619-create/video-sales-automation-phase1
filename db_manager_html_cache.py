"""
db_manager_html_cache.py
HTML キャッシュを管理する DB モジュール
"""

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path("logs/html_cache.db")

def init_html_cache_db():
    """HTML キャッシュテーブルを初期化"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS html_cache (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url_hash TEXT UNIQUE NOT NULL,
        url TEXT NOT NULL,
        html TEXT NOT NULL,
        cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP NOT NULL
    )
    """)

    # インデックス作成（URL ハッシュで高速検索）
    c.execute("""
    CREATE INDEX IF NOT EXISTS idx_url_hash ON html_cache(url_hash)
    """)

    # 有効期限インデックス（期限切れ削除用）
    c.execute("""
    CREATE INDEX IF NOT EXISTS idx_expires_at ON html_cache(expires_at)
    """)

    conn.commit()
    conn.close()

def get_cached_html(url, ttl_hours=24):
    """キャッシュから HTML を取得"""
    import hashlib
    url_hash = hashlib.md5(url.encode()).hexdigest()
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    SELECT html FROM html_cache 
    WHERE url_hash = ? AND expires_at > CURRENT_TIMESTAMP
    """, (url_hash,))
    
    result = c.fetchone()
    conn.close()

    return result[0] if result else None

def set_cached_html(url, html, ttl_hours=24):
    """HTML をキャッシュに保存"""
    import hashlib
    url_hash = hashlib.md5(url.encode()).hexdigest()
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    expires_at = datetime.now() + timedelta(hours=ttl_hours)

    c.execute("""
    INSERT OR REPLACE INTO html_cache (url_hash, url, html, expires_at)
    VALUES (?, ?, ?, ?)
    """, (url_hash, url, html, expires_at.isoformat()))

    conn.commit()
    conn.close()

def clean_expired_cache():
    """期限切れのキャッシュを削除"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("DELETE FROM html_cache WHERE expires_at <= CURRENT_TIMESTAMP")
    deleted_count = c.rowcount

    conn.commit()
    conn.close()

    return deleted_count

def get_cache_stats():
    """キャッシュ統計を取得"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT COUNT(*), SUM(LENGTH(html)) / 1024.0 FROM html_cache WHERE expires_at > CURRENT_TIMESTAMP")
    result = c.fetchone()
    conn.close()

    count = result[0] if result[0] else 0
    size_kb = result[1] if result[1] else 0

    return count, size_kb
