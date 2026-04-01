from crm_manager import LEADS_COLUMNS

print('=== LEADS_COLUMNS の全項目 ===')
for key, col_num in sorted(LEADS_COLUMNS.items(), key=lambda x: x[1]):
    print(f'{col_num:2d}: {key}')
