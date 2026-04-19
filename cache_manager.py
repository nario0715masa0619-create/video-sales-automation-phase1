"""
cache_manager.py
HTML キャッシュ管理（SQLite）
"""
import logging
import sqlite3
import os
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

CACHE_DB_PATH = 'html_cache.db'

def init_cache():
    """キャッシュ DB を初期化"""
    try:
        conn = sqlite3.connect(CACHE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS html_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                domain TEXT,
                html TEXT,
                cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        logger.info("✅ キャッシュ DB を初期化しました")
    except Exception as e:
        logger.error(f"❌ キャッシュ DB 初期化エラー: {e}")

def get_cached_html(url, ttl=24):
    """キャッシュから HTML を取得（TTL チェック付き）"""
    try:
        conn = sqlite3.connect(CACHE_DB_PATH)
        cursor = conn.cursor()
        
        now = datetime.now()
        cursor.execute('''
            SELECT html FROM html_cache 
            WHERE url = ? AND expires_at > ?
        ''', (url, now))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            logger.debug(f"💾 キャッシュヒット: {url}")
            return result[0]
        
        return None
    except Exception as e:
        logger.debug(f"キャッシュ取得エラー: {e}")
        return None

def set_cached_html(url, html, ttl=24):
    """キャッシュに HTML を保存"""
    try:
        conn = sqlite3.connect(CACHE_DB_PATH)
        cursor = conn.cursor()
        
        expires_at = datetime.now() + timedelta(hours=ttl)
        domain = url.split('/')[2]  # ドメイン抽出
        
        cursor.execute('''
            INSERT OR REPLACE INTO html_cache (url, domain, html, expires_at)
            VALUES (?, ?, ?, ?)
        ''', (url, domain, html, expires_at))
        
        conn.commit()
        conn.close()
        logger.debug(f"💾 キャッシュ保存: {url}")
        return True
    except Exception as e:
        logger.error(f"❌ キャッシュ保存エラー: {e}")
        return False

def clear_cache():
    """すべてのキャッシュをクリア"""
    try:
        conn = sqlite3.connect(CACHE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM html_cache')
        conn.commit()
        conn.close()
        logger.info("✅ キャッシュをクリアしました")
        return True
    except Exception as e:
        logger.error(f"❌ キャッシュクリアエラー: {e}")
        return False

def clear_cache_by_domain(domain):
    """ドメイン単位でキャッシュをクリア"""
    try:
        conn = sqlite3.connect(CACHE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM html_cache WHERE domain = ?', (domain,))
        conn.commit()
        conn.close()
        logger.info(f"✅ {domain} のキャッシュをクリアしました")
        return True
    except Exception as e:
        logger.error(f"❌ キャッシュクリアエラー: {e}")
        return False

def get_cache_stats():
    """キャッシュの統計情報を取得"""
    try:
        conn = sqlite3.connect(CACHE_DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM html_cache')
        count = cursor.fetchone()[0]
        
        # DB ファイルサイズ
        db_size_mb = os.path.getsize(CACHE_DB_PATH) / (1024 * 1024)
        
        conn.close()
        return count, db_size_mb
    except Exception as e:
        logger.error(f"❌ キャッシュ統計エラー: {e}")
        return 0, 0.0