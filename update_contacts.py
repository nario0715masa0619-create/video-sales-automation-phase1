import time
import logging
from crm_manager import get_crm
from email_extractor import get_email_from_youtube_channel

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

def main():
    print("=== CRM 連絡先更新スクリプト ===")

    crm = get_crm()
    ws = crm._get_sheet("Leads")

    # シートの全データを取得（行番号付き）
    all_values = ws.get_all_values()
    logger.info(f"全行数（ヘッダー含む）: {len(all_values)}")

    # チャンネルURLは J列（インデックス9）
    CHANNEL_URL_COL = 9   # 0-based index
    EMAIL_COL       = 3   # C列 (gspread: 1-based → 3)
    FORM_COL        = 4   # D列 (gspread: 1-based → 4)

    updated = 0
    skipped = 0
    failed  = 0

    for i, row in enumerate(all_values):
        if i == 0:
            continue  # ヘッダー行スキップ

        row_num = i + 1  # gspreadは1-based

        # チャンネルURL取得
        channel_url = row[CHANNEL_URL_COL].strip() if len(row) > CHANNEL_URL_COL else ""
        if not channel_url or not channel_url.startswith("http"):
            continue

        # ▼▼ 追加：A列（会社名）をチャンネル名で補完 ▼▼
        channel_name = row[10].strip() if len(row) > 10 else ""
        current_company = row[0].strip() if len(row) > 0 else ""
        if not current_company and channel_name:
            ws.update_cell(row_num, 1, channel_name)
            time.sleep(0.5)
        # ▲▲ 追加ここまで ▲▲

        # すでにメールまたはフォームURLが入っていればスキップ
        current_email    = row[2].strip() if len(row) > 2 else ""  # C列(index2)
        current_form_url = row[3].strip() if len(row) > 3 else ""  # D列(index3)
        if current_email or current_form_url:
            skipped += 1
            logger.info(f"スキップ（設定済み）: {channel_url}")
            continue

        logger.info(f"--- {updated+failed+1}: {channel_url} ---")

        try:

            website, email, form_url = get_email_from_youtube_channel(channel_url)

            if email or form_url:
                # ✅ gspread で直接セルを更新
                if email:
                    ws.update_cell(row_num, EMAIL_COL, email)
                    time.sleep(0.5)
                if form_url:
                    ws.update_cell(row_num, FORM_COL, form_url)
                    time.sleep(0.5)
                updated += 1
                logger.info(f"✅ 更新: email={email or 'なし'}, form={form_url or 'なし'}")
            else:
                # 取得失敗マークをC列に書き込む
                ws.update_cell(row_num, EMAIL_COL, "×取得失敗")
                time.sleep(0.5)
                failed += 1
                logger.info(f"❌ 取得失敗マーク記入: {channel_url}")
        except Exception as e:
            failed += 1
            logger.error(f"エラー [{channel_url}]: {e}")

        time.sleep(2)  # API レート制限対策

    print(f"\n=== 完了 ===")
    print(f"✅ 更新: {updated}件")
    print(f"⏭  スキップ: {skipped}件")
    print(f"❌ 失敗: {failed}件")

if __name__ == "__main__":
    main()
