from crm_manager import get_crm_manager

crm = get_crm_manager()
sheet = crm.sheet

print('=== Google Sheets の最初の 10 行 ===')
values = sheet.get_all_values()
for i, row in enumerate(values[:10]):
    print(f'{i+1}: {row[:5]}...')  # 最初の 5 列だけ表示
