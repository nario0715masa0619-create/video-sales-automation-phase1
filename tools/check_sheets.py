import gspread
from google.oauth2.service_account import Credentials

creds = Credentials.from_service_account_file('credentials/service_account.json')
client = gspread.authorize(creds)
sheet = client.open('SNS動画活用企業向け営業CRM管理シート').sheet1

# ヘッダー行を確認
print('=== ヘッダー行 ===')
for i, cell in enumerate(sheet.row_values(1)):
    print(f'{i+1}: {cell}')

# 最初の2行のデータを確認
print('\\n=== 最初の2行 ===')
for row_num in [2, 3]:
    print(f'Row {row_num}: {sheet.row_values(row_num)[:15]}')
