import sys
sys.path.insert(0, '.')

import sqlite3
import logging
from crm_manager import append_to_gsheet_phase5
import time

# ログ設定（UTF-8 エンコーディング）
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/import_to_gsheet.log', encoding='utf-8'),
    ]
)
logger = logging.getLogger(__name__)

# DB から全データを取得
conn = sqlite3.connect('logs/phase5_data.db')
cursor = conn.cursor()
cursor.execute('SELECT company_name, phone_number, email, status, website_url FROM phase5_data ORDER BY rowid DESC')
rows = cursor.fetchall()
conn.close()

print(f'DB から {len(rows)} 件のデータを読み込みました')

# スプシに保存
success = 0
failed = 0

for i, row in enumerate(rows, 1):
    company_name, phone_number, email, status, website_url = row
    try:
        result = append_to_gsheet_phase5(company_name, phone_number, email, status, website_url)
        if result:
            success += 1
        else:
            failed += 1
        
        if i % 10 == 0:
            print(f'進捗: {i}/{len(rows)} - 成功: {success} / 失敗: {failed}')
    except Exception as e:
        failed += 1
        logger.error(f'Row {i} error ({company_name}): {str(e)[:100]}')
    
    time.sleep(5)  # 5 秒待機（レート制限対策）

print(f'================================================================================')
print(f'インポート完了: 成功 {success} 件 / 失敗 {failed} 件')
print(f'================================================================================')
