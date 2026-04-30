import sys
sys.path.insert(0, '.')

import sqlite3
import logging
from crm_manager import append_to_gsheet_phase5
import time

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/import_to_gsheet.log', encoding='utf-8'),
    ]
)
logger = logging.getLogger(__name__)

# スプシに既に保存されたデータを取得
import gspread
from config import SPREADSHEET_ID_PHASE5, SHEET_NAME_PHASE5

gc = gspread.service_account(filename='credentials/service_account.json')
sh = gc.open_by_key(SPREADSHEET_ID_PHASE5)
ws = sh.worksheet(SHEET_NAME_PHASE5)
saved_urls = set([row[1] if len(row) > 1 else '' for row in ws.get_all_values()[1:]])  # website_url (2列目)

print(f'スプシに既に保存された URL: {len(saved_urls)} 件')

# DB から未保存データを取得
conn = sqlite3.connect('logs/phase5_data.db')
cursor = conn.cursor()
cursor.execute('SELECT company_name, phone_number, email, status, website_url FROM phase5_data')
all_rows = cursor.fetchall()
conn.close()

# 未保存データをフィルタリング
rows_to_save = [row for row in all_rows if row[4] not in saved_urls]
print(f'未保存データ: {len(rows_to_save)} 件')

# スプシに保存
success = 0
failed = 0
start_time = time.time()

for i, row in enumerate(rows_to_save, 1):
    company_name, phone_number, email, status, website_url = row
    try:
        result = append_to_gsheet_phase5(company_name, phone_number, email, status, website_url)
        if result:
            success += 1
        else:
            failed += 1
        
        if i % 50 == 0:
            elapsed = time.time() - start_time
            rate = i / elapsed
            remaining = (len(rows_to_save) - i) / rate
            print(f'進捗: {i}/{len(rows_to_save)} ({i*100//len(rows_to_save)}%) - 成功: {success} - 残り: {int(remaining)}秒')
    except Exception as e:
        failed += 1
        logger.error(f'Error: {company_name}: {str(e)[:100]}')
    
    time.sleep(1)  # 1 秒待機

elapsed = time.time() - start_time
print(f'================================================================================')
print(f'完了: 成功 {success} 件 / 失敗 {failed} 件')
print(f'所要時間: {int(elapsed)} 秒 ({int(elapsed/60)} 分 {int(elapsed%60)} 秒)')
print(f'================================================================================')
