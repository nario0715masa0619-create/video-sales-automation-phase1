from crm_manager import CRMManager, LEADS_COLUMNS
import config

crm = CRMManager()
sheet = crm._get_sheet(config.SHEET_LEADS)
all_values = sheet.get_all_values()

# 送信済みのチャンネル名
sent_channels = [
    '腕時計と僕。Y',
    'AFL JAPAN / 日本オーストラリアンフットボール協会',
    'くろろじちゃんねる',
    'テストチャンネル'
]

# 各チャンネルのステータスを更新
status_col = LEADS_COLUMNS.get('送信ステータス', 17)
print(f'送信ステータス列: {status_col}')

for i, row in enumerate(all_values):
    if len(row) > 0 and row[0] in sent_channels:
        row_num = i + 1
        sheet.update_cell(row_num, status_col, 'sent')
        print(f'✅ {row[0]} のステータスを「sent」に更新しました')
