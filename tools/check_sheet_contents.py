import gspread
from google.oauth2.service_account import Credentials

scopes = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file('credentials/service_account.json', scopes=scopes)
client = gspread.authorize(creds)
sheet = client.open('SNS動画活用企業向け営業CRM管理シート').sheet1

print('=== Google Sheets (最初の 10 行) ===')
values = sheet.get_all_values()
for i, row in enumerate(values[:10]):
    print(f'{i+1}: {row}')
