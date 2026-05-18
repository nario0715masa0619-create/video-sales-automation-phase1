import gspread
from config import SPREADSHEET_ID
from datetime import datetime, timedelta, timezone

JST = timezone(timedelta(hours=9))
gc = gspread.service_account(filename='credentials/service_account.json')
sheet = gc.open_by_key(SPREADSHEET_ID).sheet1
rows = sheet.get_all_records()

kintone = [r for r in rows if 'kintone活用ちゃんねる' in r.get('チャンネル名', '')][0]
print(f"送信回数: {kintone.get('送信回数')}")
print(f"最終送信日: {kintone.get('最終送信日')}")
