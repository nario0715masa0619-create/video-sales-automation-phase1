from crm_manager import get_gsheet_client
from config import SPREADSHEET_ID, SHEET_NAME_CRM

client = get_gsheet_client()
spreadsheet = client.open_by_key(SPREADSHEET_ID)
worksheet = spreadsheet.worksheet(SHEET_NAME_CRM)
rows = worksheet.get_all_values()

print("ヘッダ行（行1）:")
print(rows[0])
print("\n最初の3行のデータ:")
for i in range(1, min(4, len(rows))):
    print(f"行{i+1}: {rows[i]}")
