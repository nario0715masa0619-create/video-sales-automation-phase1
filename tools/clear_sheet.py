import gspread
from google.oauth2.service_account import Credentials

scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file('credentials/service_account.json', scopes=scopes)
client = gspread.authorize(creds)

sheet = client.open('SNS動画活用企業向け営業CRM管理シート').sheet1
sheet.batch_clear(['A2:ZZ10000'])

print('✅ Google Sheets をクリアしました')
