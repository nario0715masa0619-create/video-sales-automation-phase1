from crm_manager import get_crm

crm = get_crm()
sheet = crm._get_sheet("営業リード")

print("=== Google Sheets の内容 ===")
values = sheet.get_all_values()
print(f"Total rows: {len(values)}")
print()

# ヘッダーと最初の 5 行を表示
for i, row in enumerate(values[:6]):
    if i == 0:
        print(f"Header: {row}")
    else:
        print(f"Row {i}: {row[:8]}...")
