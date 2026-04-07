with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# to_crm_dict と upsert_lead を呼び出している箇所を探す
for i, line in enumerate(lines):
    if 'to_crm_dict' in line or ('upsert_lead' in line and 'crm_mgr' in line):
        # 前後の行を表示
        for j in range(max(0, i-2), min(i+3, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        print('---')
