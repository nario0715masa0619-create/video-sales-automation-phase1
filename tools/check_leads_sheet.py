from crm_manager import get_crm

crm = get_crm()
sheet = crm._get_sheet("Leads")

print("=== Google Sheets Leads シートの内容 ===")
values = sheet.get_all_values()
print(f"Total rows: {len(values)}")
print()

# ヘッダーと最初の 6 行を表示
for i, row in enumerate(values[:6]):
    if i == 0:
        print(f"Header: {row[:10]}")
    else:
        # メールアドレス列（インデックス 6）を確認
        email = row[6] if len(row) > 6 else "NONE"
        print(f"Row {i}: {row[1]} | Email: {email}")
