with open('crm_manager.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# get_leads_for_email の前後 5 行を表示
for i, line in enumerate(lines):
    if 'def get_leads_for_email' in line:
        print(f'=== get_leads_for_email 周辺 ===')
        for j in range(max(0, i-5), min(len(lines), i+10)):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
else:
    print('get_leads_for_email が見つかりません')
