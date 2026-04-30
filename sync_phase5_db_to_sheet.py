import sqlite3
import logging
import sys
from config import SPREADSHEET_ID_PHASE5, SHEET_NAME_PHASE5
from crm_manager import get_crm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler(sys.stdout)])

def sync_phase5_db_to_sheet():
    logger = logging.getLogger(__name__)
    logger.info("Phase 5: DBのデータをGoogleシートに完全同期します...")

    # DBから全データを取得
    conn = sqlite3.connect('logs/phase5_data.db')
    c = conn.cursor()
    c.execute("""
        SELECT company_name, website_url, phone_number, email, status, scraped_at, 
               contact_form_url, remarks, validation_status, validation_score
        FROM phase5_data
        ORDER BY id ASC
    """)
    rows = c.fetchall()
    conn.close()

    if not rows:
        logger.warning("同期するデータがDBにありません。")
        return

    # Google Sheets クライアント取得
    crm = get_crm()
    client = crm._get_client()
    spreadsheet = client.open_by_key(SPREADSHEET_ID_PHASE5)
    worksheet = spreadsheet.worksheet(SHEET_NAME_PHASE5)

    # データを2次元配列に整形
    headers = [
        "Company Name", "URL", "Phone", "Email", "Source Page", "Status", "Scraped At",
        "Contact Form URL", "Remarks", "Validation Status", "Validation Score", "CRM Sync Decision"
    ]
    
    sheet_data = [headers]
    for r in rows:
        v_status = r[8]
        v_score = r[9] if r[9] is not None else 0
        
        # 同期判定のラベル作成
        if v_status == "valid":
            decision = "OK: Valid"
        elif v_status == "catch-all":
            if v_score >= 80:
                decision = "OK: Catch-all (High Score)"
            else:
                decision = "Excluded: Low Score Catch-all"
        elif v_status == "invalid":
            decision = "Excluded: Invalid"
        elif v_status == "test_email":
            decision = "Excluded: Test/Dummy"
        elif v_status is None or v_status == "":
            decision = "Pending"
        else:
            decision = f"Excluded: {v_status}"

        sheet_data.append([
            r[0] if r[0] is not None else "",
            r[1] if r[1] is not None else "",
            r[2] if r[2] is not None else "",
            r[3] if r[3] is not None else "None",
            r[1] if r[1] is not None else "",  # source_page (URLと同じ値)
            r[4] if r[4] is not None else "",
            r[5] if r[5] is not None else "",
            r[6] if r[6] is not None else "None",
            r[7] if r[7] is not None else "",
            v_status if v_status is not None else "",
            v_score if v_score != 0 else "",
            decision
        ])

    # Google Sheetsの一括上書き
    try:
        # 古いバージョンと新しいバージョンの互換性のため
        try:
            worksheet.clear()
            worksheet.update('A1', sheet_data)
        except Exception:
            worksheet.clear()
            worksheet.update(values=sheet_data, range_name='A1')
            
        logger.info(f"✅ {len(rows)} 件のデータをPhase 5シートに同期完了しました！")
    except Exception as e:
        logger.error(f"❌ シートの更新中にエラーが発生しました: {e}")

if __name__ == "__main__":
    sync_phase5_db_to_sheet()
