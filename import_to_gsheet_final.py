import sys
sys.path.insert(0, '.')
import sqlite3, gspread, time, logging
from datetime import datetime

logging.basicConfig(
    filename='logs/import_to_gsheet_final.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger()

# config.py から SPREADSHEET_ID と SHEET_NAME を読み込む
import config
SPREADSHEET_ID = config.SPREADSHEET_ID_PHASE5
SHEET_NAME = config.SHEET_NAME_PHASE5

logger.info('=== インポート開始 ===')
print('スプシ接続中...')

# スプレッドシートを **一度だけ** 開く
try:
    gc = gspread.service_account(filename='credentials/service_account.json')
    sh = gc.open_by_key(SPREADSHEET_ID)
    ws = sh.worksheet(SHEET_NAME)
    logger.info('✅ スプシ接続完了')
    print('✅ スプシ接続完了')
except Exception as e:
    logger.error(f'❌ スプシ接続失敗: {e}')
    print(f'❌ スプシ接続失敗: {e}')
    sys.exit(1)

# 既存 URL を取得
print('既存データを読み込み中...')
try:
    all_rows = ws.get_all_values()
    existing_urls = {row[1] for row in all_rows[1:] if len(row) > 1 and row[1]}
    logger.info(f'✅ 既存 URL 数: {len(existing_urls)}')
    print(f'✅ 既存 URL 数: {len(existing_urls)}')
except Exception as e:
    logger.error(f'既存 URL 取得失敗: {e}')
    print(f'⚠️  既存 URL 取得失敗: {e}')
    existing_urls = set()

# DB から全行を取得
print('DB から未保存行を抽出中...')
conn = sqlite3.connect('logs/phase5_data.db')
cursor = conn.cursor()
cursor.execute('SELECT company_name, phone_number, email, status, website_url FROM phase5_data ORDER BY rowid DESC')
all_db_rows = cursor.fetchall()
conn.close()

# 未保存行のみフィルタ
rows = [r for r in all_db_rows if r[4] not in existing_urls]
logger.info(f'未保存行数: {len(rows)}')
print(f'未保存行数: {len(rows)}')

if not rows:
    print('✅ 全データが既に保存されています')
    logger.info('全データが既に保存されています')
    sys.exit(0)

success, failed = 0, 0
start_time = time.time()
print(f'\n開始: {datetime.now().strftime("%H:%M:%S")}\n')

for idx, (company, phone, email, status, url) in enumerate(rows, 1):
    try:
        row_data = [
            company,
            url,
            phone if phone else 'None',
            email if email else 'None',
            '',
            status,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ]
        ws.append_row(row_data)
        success += 1
        
        if idx % 50 == 0:
            elapsed = time.time() - start_time
            remaining_rows = len(rows) - idx
            remaining_secs = remaining_rows * 2
            remaining_mins = int(remaining_secs // 60)
            percent = int(100 * idx / len(rows))
            
            msg = f'進捗: {idx}/{len(rows)} ({percent}%) - 成功: {success} - 残り時間: {remaining_mins} 分'
            logger.info(msg)
            print(msg)
        
        time.sleep(2)  # レート制限回避
        
    except Exception as e:
        failed += 1
        logger.error(f'エラー (行 {idx}, {company[:20]}): {str(e)[:80]}')
        time.sleep(3)  # エラー時は長めに待機

elapsed = time.time() - start_time
msg_final = f'完了: 成功 {success}, 失敗 {failed}, 経過時間 {int(elapsed//60)} 分 {int(elapsed%60)} 秒'
logger.info(msg_final)
print(f'\n✅ {msg_final}')
