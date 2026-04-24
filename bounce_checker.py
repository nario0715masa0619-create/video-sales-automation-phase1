#!/usr/bin/env python3
"""
Phase 6: ZeroBounce Email Validation
メールアドレスをZeroBounceで検証し、スコアを DB に保存
改善版：catch-all は有効扱い、テスト用ドメインは除外、クレジット切れで中断
"""

import sqlite3
import logging
import requests
from datetime import datetime
from pathlib import Path
import time
import sys
from config import ZEROBOUNCE_API_KEY, ZEROBOUNCE_API_URL

# ===== Configuration =====
DB_PATH = "logs/phase5_data.db"

# テスト用ドメイン・メールアドレス（除外対象）
TEST_DOMAINS = [
    'example.com',
    'test.com',
    'sample.com',
    'xx.co.jp',
    'localhost',
    'invalid.com',
    'wixpress.com',  # Wix 自動生成アドレス
    'sentry',        # Sentry の自動生成アドレス
]

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

class InsufficientCreditsError(Exception):
    """ZeroBounce クレジット切れエラー"""
    pass

def is_test_email(email: str) -> bool:
    """テスト用メールアドレスかどうか判定"""
    if not email:
        return False
    email_lower = email.lower()
    for test_domain in TEST_DOMAINS:
        if test_domain in email_lower:
            return True
    return False

def validate_email_with_zerobounce(email: str) -> dict:
    """ZeroBounce API でメールアドレスを検証"""
    params = {
        "email": email,
        "api_key": ZEROBOUNCE_API_KEY
    }
    
    try:
        response = requests.get(ZEROBOUNCE_API_URL, params=params, timeout=10)
        data = response.json()
        
        # クレジット切れ判定
        if "error" in data:
            error_msg = data.get("error", "").lower()
            if "credit" in error_msg or "insufficient" in error_msg:
                logger.error(f"❌ ZeroBounce クレジット切れ: {data.get('error')}")
                raise InsufficientCreditsError(data.get("error"))
            else:
                logger.error(f"ZeroBounce API エラー: {data.get('error')}")
                return {
                    "status": "error",
                    "score": 0,
                    "is_valid": False
                }
        
        # 結果を標準化
        status = data.get("status")
        score = data.get("confidence_score", 0)
        
        # catch-all は有効扱い、valid も有効、それ以外は無効
        is_valid = status in ["valid", "catch-all"]
        
        return {
            "status": status,
            "sub_status": data.get("sub_status"),
            "score": score,
            "is_valid": is_valid
        }
    except InsufficientCreditsError:
        raise
    except Exception as e:
        logger.error(f"ZeroBounce API エラー: {e}")
        return {
            "status": "error",
            "score": 0,
            "is_valid": False
        }

def init_phase6_db():
    """Phase 6 用カラムをDBに追加（存在しなければ）"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    try:
        cur.execute("ALTER TABLE phase5_data ADD COLUMN validation_status TEXT")
        logger.info("✅ validation_status カラムを追加")
    except sqlite3.OperationalError:
        logger.debug("validation_status カラムは既に存在")
    
    try:
        cur.execute("ALTER TABLE phase5_data ADD COLUMN validation_score INTEGER")
        logger.info("✅ validation_score カラムを追加")
    except sqlite3.OperationalError:
        logger.debug("validation_score カラムは既に存在")
    
    try:
        cur.execute("ALTER TABLE phase5_data ADD COLUMN validation_at TIMESTAMP")
        logger.info("✅ validation_at カラムを追加")
    except sqlite3.OperationalError:
        logger.debug("validation_at カラムは既に存在")
    
    conn.commit()
    conn.close()

def run_phase6_validation(limit=100):
    """Phase 5 から最大 limit 件のメールを検証"""
    init_phase6_db()
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # 未検証のメール（validation_status が NULL）を取得
    cur.execute("""
        SELECT id, company_name, email FROM phase5_data 
        WHERE email IS NOT NULL 
        AND validation_status IS NULL
        LIMIT ?
    """, (limit,))
    
    records = cur.fetchall()
    logger.info(f"📧 {len(records)} 件のメールアドレスを検証開始")
    
    valid_count = 0
    invalid_count = 0
    error_count = 0
    test_count = 0
    
    try:
        for idx, (record_id, company_name, email) in enumerate(records, 1):
            logger.info(f"[{idx}/{len(records)}] {company_name} | {email}")
            
            # テスト用メールアドレスを除外
            if is_test_email(email):
                logger.info(f"   ⚠️  テスト用メールアドレス（除外）")
                cur.execute("""
                    UPDATE phase5_data 
                    SET validation_status = ?, 
                        validation_score = ?,
                        validation_at = ?
                    WHERE id = ?
                """, (
                    "test_email",
                    0,
                    datetime.now().isoformat(),
                    record_id
                ))
                conn.commit()
                test_count += 1
                continue
            
            result = validate_email_with_zerobounce(email)
            
            # DB に検証結果を保存
            cur.execute("""
                UPDATE phase5_data 
                SET validation_status = ?, 
                    validation_score = ?,
                    validation_at = ?
                WHERE id = ?
            """, (
                result["status"],
                result["score"],
                datetime.now().isoformat(),
                record_id
            ))
            conn.commit()
            
            if result["is_valid"]:
                valid_count += 1
                logger.info(f"   ✅ 有効 (status: {result['status']}, スコア: {result['score']})")
            elif result["status"] == "error":
                error_count += 1
                logger.warning(f"   ⚠️  検証エラー")
            else:
                invalid_count += 1
                logger.info(f"   ❌ 無効 ({result['status']}, スコア: {result['score']})")
            
            # API レート制限対応（1リクエスト/秒）
            time.sleep(1)
    
    except InsufficientCreditsError as e:
        conn.close()
        logger.error("=" * 80)
        logger.error("🚨 ZeroBounce クレジット切れで中断しました")
        logger.error("=" * 80)
        logger.error(f"処理状況: 有効 {valid_count}件 / 無効 {invalid_count}件 / エラー {error_count}件 / テスト除外 {test_count}件")
        logger.error("")
        logger.error("【対応方法】")
        logger.error("1. ZeroBounce ダッシュボード（https://www.zerobounce.net/）にログイン")
        logger.error("2. Billing → クレジットをチャージ")
        logger.error("3. 下記コマンドで再実行：")
        logger.error(f"   python bounce_checker.py {limit}")
        logger.error("=" * 80)
        sys.exit(1)
    
    conn.close()
    
    logger.info("=" * 80)
    logger.info(f"✅ 検証完了: 有効 {valid_count}件 / 無効 {invalid_count}件 / エラー {error_count}件 / テスト除外 {test_count}件")
    logger.info("=" * 80)

if __name__ == "__main__":
    import sys
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    run_phase6_validation(limit)
