import sqlite3
import gspread
import config
import time

print('Phase 5 email address CRM overwrite in progress...')

# Google Sheets 接続（CRM）
gc = gspread.service_account(filename='credentials/service_account.json')
crm_sh = gc.open_by_key(config.SPREADSHEET_ID)
crm_ws = crm_sh.worksheet(config.SHEET_LEADS)

# Phase 5 DB からメールアドレスを取得
conn = sqlite3.connect('logs/phase5_data.db')
c = conn.cursor()
c.execute('''
    SELECT website_url, email FROM phase5_data 
    WHERE email IS NOT NULL AND email != "None"
    AND (
        validation_status = "valid" 
        OR (validation_status = "catch-all" AND validation_score >= 80)
    )
''')
phase5_emails = {row[0]: row[1] for row in c.fetchall()}
conn.close()

print(f'Phase 5 メール数: {len(phase5_emails)} 件')

# CRM シートの全データを取得
crm_rows = crm_ws.get_all_values()
print(f'CRM 総行数: {len(crm_rows)} 件')

# カラム（0-indexed）
email_col = 2              # 3列目: メールアドレス
website_col = 4            # 5列目: 公式サイト
send_count_col = 25        # 26列目: 送信回数
send_date_cols = [26, 27, 28, 29, 30]  # 27-31列目: 送信日

# 更新リクエスト作成
requests = []
new_email_count = 0
replaced_email_count = 0

for row_idx in range(1, len(crm_rows)):
    row = crm_rows[row_idx]
    crm_website = row[website_col] if website_col < len(row) else None
    crm_email = row[email_col] if email_col < len(row) else None
    
    if crm_website in phase5_emails:
        new_email = phase5_emails[crm_website]
        
        if not crm_email or crm_email.strip() == '':
            # メールが空 → そのまま上書き
            requests.append({
                'updateCells': {
                    'rows': [{
                        'values': [{'userEnteredValue': {'stringValue': new_email}}]
                    }],
                    'fields': 'userEnteredValue',
                    'start': {'sheetId': crm_ws.id, 'rowIndex': row_idx, 'columnIndex': email_col}
                }
            })
            new_email_count += 1
        else:
            # メールがある → 上書き + 送信履歴をクリア
            values = [{'userEnteredValue': {'stringValue': new_email}}]
            values.append({'userEnteredValue': {'stringValue': '0'}})
            for _ in send_date_cols:
                values.append({'userEnteredValue': {'stringValue': ''}})
            
            requests.append({
                'updateCells': {
                    'rows': [{'values': values}],
                    'fields': 'userEnteredValue',
                    'start': {'sheetId': crm_ws.id, 'rowIndex': row_idx, 'columnIndex': email_col}
                }
            })
            replaced_email_count += 1

total_updated = new_email_count + replaced_email_count
print(f'更新対象: {total_updated} 件')
print(f'   新規メール追加: {new_email_count} 件')
print(f'   メール置き換え + 履歴クリア: {replaced_email_count} 件')

# バッチ更新（10 リクエストごと、3 秒待機）
if requests:
    for i in range(0, len(requests), 10):
        batch = requests[i:i+10]
        body = {'requests': batch}
        crm_sh.batch_update(body)
        print(f'更新中... {min(i+10, len(requests))}/{len(requests)} リクエスト')
        time.sleep(3)  # API レート制限対策

print('Done')
print(f'   新規メール追加: {new_email_count} 件')
print(f'   メール置き換え + 履歴クリア: {replaced_email_count} 件')
