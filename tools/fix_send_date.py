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

# 各チャンネルの送信日を修正
send_date_col = LEADS_COLUMNS.get('1通目送信日', 26)
now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

for i, row in enumerate(all_values):
    if len(row) > 0 and row[0] in sent_channels:
        row_num = i + 1
        sheet.update_cell(row_num, send_date_col, now_str)
        print(f'✅ {row[0]} の「1通目送信日」を「{now_str}」に修正しました')
