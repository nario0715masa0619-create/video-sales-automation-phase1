from crm_manager import CRMManager
import config

crm = CRMManager()

# Google Sheets の全列を確認
sheet = crm._get_sheet(config.SHEET_LEADS)
headers = sheet.row_values(1)

print("Google Sheets の列一覧:")
for idx, header in enumerate(headers, 1):
    print(f"  列 {idx}: {header}")

# メール送信回数の列番号を確認
if "メール送信回数" in headers:
    col_num = headers.index("メール送信回数") + 1
    print(f"\nメール送信回数は列 {col_num} にあります")
else:
    print(f"\nメール送信回数が見つかりません")
