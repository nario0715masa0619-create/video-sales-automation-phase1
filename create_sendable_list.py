#!/usr/bin/env python3
"""
Phase 6 完了後の送信対象リスト作成スクリプト
Phase 5 Google Sheet の新しいタブ「送信対象」に出力
"""

import sqlite3
import logging
from datetime import datetime
from crm_manager import get_crm

# ===== Configuration =====
DB_PATH = "logs/phase5_data.db"
SENDABLE_LIST_SHEET = "送信対象"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

def create_sendable_list_in_sheet():
    """Phase 6 検証済みで送信可能なメールアドレスを Google Sheet に出力"""
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # 検証済みで有効なメール（valid, catch-all）を抽出
    cur.execute("""
        SELECT 
            id,
            company_name,
            phone_number,
            email,
            validation_status,
            validation_score,
            validation_at
        FROM phase5_data
        WHERE validation_status IN ('valid', 'catch-all')
        ORDER BY id
    """)
    
    records = cur.fetchall()
    conn.close()
    
    logger.info(f"📊 送信対象リスト作成開始")
    logger.info(f"対象件数: {len(records)}件（検証済み有効アドレス）")
    
    if not records:
        logger.warning("検証済み有効アドレスがありません")
        return
    
    # ===== Google Sheet に追記 =====
    try:
        crm = get_crm()
        
        # Phase 5 シートから送信対象シートを取得 or 作成
        # TODO: 既存シートがあるか確認して作成 or 削除して再作成
        
        # ヘッダー行を作成
        header = ["ID", "会社名", "電話番号", "メールアドレス", "検証ステータス", "検証スコア", "検証日時"]
        
        # Google Sheet への追記処理（実装待ち）
        logger.info(f"✅ Google Sheet に {len(records)}件を追記します")
        logger.warning("⚠️  Google Sheets API 統合待ち（実装予定）")
        
        # 統計情報
        valid_count = sum(1 for r in records if r[4] == 'valid')
        catchall_count = sum(1 for r in records if r[4] == 'catch-all')
        
        logger.info("=" * 80)
        logger.info("📊 リスト作成完了")
        logger.info(f"  送信可能メール: {len(records)}件")
        logger.info(f"    - valid: {valid_count}件")
        logger.info(f"    - catch-all: {catchall_count}件")
        logger.info(f"  出力先: Google Sheet「Phase 5」の「{SENDABLE_LIST_SHEET}」タブ")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_sendable_list_in_sheet()
