from crm_manager import CRMManager, LEADS_COLUMNS
import config
from datetime import datetime

crm = CRMManager()
sheet = crm._get_sheet(config.SHEET_LEADS)
all_values = sheet.get_all_values()

# 送信済みのチャンネル名
sent_channels = [
    '腕時計と僕。Y',
    'AFL JAPAN / 日本オーストラリアンフットボール協会',
    'くろろじちゃんねる',
]

# 各チャンネルを更新
status_col = LEADS_COLUMNS.get('営業ステータス', 24)
send_count_col = LEADS_COLUMNS.get('メール送信回数', 25)
send_date_col = LEADS_COLUMNS.get('1通目送信日', 26)
today = datetime.now().strftime('%Y-%m-%d')

for i, row in enumerate(all_values):
    if len(row) > 0 and row[0] in sent_channels:
        row_num = i + 1
        # 営業ステータスを「接触中」に
        sheet.update_cell(row_num, status_col, '接触中')
        # メール送信回数を「1」に
        sheet.update_cell(row_num, send_count_col, '1')
        # 1通目送信日を今日に
        sheet.update_cell(row_num, send_date_col, today)
        print(f'✅ {row[0]} を更新しました（営業ステータス: 接触中、メール送信回数: 1、1通目送信日: {today}）')
